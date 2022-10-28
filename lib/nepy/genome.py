from matplotlib import pyplot as plt

from network.connection import Connection
from network.node import Node

import random

class Genome:

    def __init__(self, sensor_size, actuator_size, innovation_method):
        self.sensor_size = sensor_size
        self.actuator_size = actuator_size
        self.nodes = []
        self.connections = []
        
        self.innovation_method = innovation_method

        # TODO: Implement hidden layer init
        self.largest_node_id = 0
        # ========== NODES LIST ========== #
        for _ in range(sensor_size):  # Sensor nodes
            self.nodes.append(self.get_new_node(node_type = 0, layer = 1))

        self.nodes.append(self.get_new_node(node_type = 3, layer = 1))  # Bias node in the input layer

        for _ in range(actuator_size):  # Actuator nodes
            self.nodes.append(self.get_new_node(node_type = 1, layer = 2))
        # ================================ #

        # ======= CONNECTIONS LIST ======= #
        for node_out in self.nodes:
            if node_out.type_ == 1:
                for node_in in self.nodes:
                    if node_in.type_ == 0 or node_in.type_ == 3:
                        self.connections.append(Connection(node_in, node_out,
                                                           innovation_number = innovation_method(node_in.name,
                                                                                                 node_out.name)))
        # ================================ #

        self.species_id = None

    def __iter__(self):
        for connection in self.connections:
            yield connection

    def __getitem__(self, item):
        for connection in self:
            if connection.innovation_number == item:
                return connection

        return None

    def __str__(self):
        return "".join(f"{str(connection)}\n" for connection in self)

    def add_node(self):
        pass

    def add_connection(self, node_in, node_out, weight):
        new_connection = Connection(node_in, node_out, weight,
                            innovation_number = self.innovation_method(node_in.name,
                                                                node_out.name))
        self.connections.append(new_connection)

    def mutate(self, weight_mutation_rate = 1, connection_mutation_rate = 0.05, connection_enable_rate = 0.25, connection_attempt_count = 20, node_mutation_rate = 0.05):
        chance = random.uniform(0,1)
        
        #weight mutation
        if weight_mutation_rate > chance:
            connection = random.choice(self.connections)
            mutation_type_chance = random.uniform(0,1)
            if mutation_type_chance > 0.9:
                # weight modification
                modification_rate = random.uniform(0.8,1.2)
                connection.weight = connection.weight * modification_rate
            else:
                #random weight assignment
                connection.weight = random.uniform(0,1)
        #adding a connection
        add_conn_chance = random.uniform(0,1)
        if connection_mutation_rate > add_conn_chance:
            for _ in range(connection_attempt_count):
                node_list = self.nodes.copy()
                node_in = random.choice(node_list)
                node_list.remove(node_in)
                node_out = random.choice(node_list)
                
                #condition on illegal, disabled and recurrent connections
                if not((node_out.layer == node_in.layer) or (node_in.layer > node_out.layer)):
                    connection = self._get_connection(node_in,node_out)
                    
                    if connection == None:
                        weight = random.uniform(0,1)
                        self.add_connection(node_in,node_out,weight)
                    elif not(connection.enable):
                        enable_chance = random.uniform(0, 1)
                        if connection_enable_rate > enable_chance:
                            connection.table = True          
        #adding a node
        node_chance = random.uniform(0,1)
        if node_mutation_rate > node_chance:
            conn_to_disable = random.choice(self.connections)
            while conn_to_disable.is_recurrent:
                conn_to_disable = random.choice(self.connections)
            conn_to_disable.enable = False
            
            innode = conn_to_disable.in_node
            outnode = conn_to_disable.out_node
            
            new_node = self.get_new_node(node_type = 2)
            
            #first connection
            self.add_connection(innode, new_node, conn_to_disable.weight)
            self.add_connection(new_node, outnode, weight = 1)
            
            # TODO: Implement node layer setting
            
    def _load_inputs(self, input_array):
        for i, input in enumerate(input_array):
            self.nodes[i].input = input
            self.nodes[i].activate()

        self.nodes[i + 1].input = 1.0
        self.nodes[i + 1].activate()

    def _get_outputs(self):
        outputs = []
        for out_node in self.nodes[self.sensor_size + 1:self.sensor_size + self.actuator_size + 1]:
            outputs.append(out_node.output)

        return outputs

    def _get_nodes_in_layer(self, layer):
        nodes_in_layer = []
        for node in self.nodes:
            if node.layer == layer:
                nodes_in_layer.append(node)

        return nodes_in_layer

    def _get_connection_ends_with(self, node):
        for connection in self.connections:
            if connection.out_node == node:
                yield connection

    def _get_connection(self, in_node, out_node):
        for connection in self.connections:
            if (connection.in_node == in_node) and (connection.out_node == out_node):
                return connection

    def forward(self, input_array):
        self._load_inputs(input_array)
        current_layer = 2

        nodes_in_layer = self._get_nodes_in_layer(current_layer)
        while nodes_in_layer:
            for node in nodes_in_layer:
                node_sum = 0
                for connection in self._get_connection_ends_with(node):
                    if connection.enable:
                        node_sum += connection.in_node.output * connection.weight
                node.input = node_sum
                node.activate()

            current_layer += 1
            nodes_in_layer = self._get_nodes_in_layer(current_layer)
        return self._get_outputs()

    def get_new_node(self, node_type, layer=None):
        self.largest_node_id += 1
        return Node(self.largest_node_id, node_type, layer = layer)

    def find_connection(self, innovation_number):
        for connection in self.connections:
            if connection.innovation_number == innovation_number:
                return connection
        return None

    def get_innovation_list(self):
        inv_list = []
        for conn in self.connections:
            inv_list.append(conn.innovation_number)
        return inv_list
    
    def draw_network(self):
        layer_dict = {}
        for node in self.nodes:
            layer = node.layer
            if layer in layer_dict.keys():
                layer_dict[layer].append(node)
            else:
                layer_dict[layer] = [node]

        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.axis("off")

        node_location_dict = {}

        ax.set_xlim(right = 15)
        ax.set_ylim(top = 10)

        x_gap = ax.get_xlim()[1] / max(layer_dict)
        x_padding = x_gap / 2
        x = x_padding

        for layer, nodes in sorted(layer_dict.items()):

            y_gap = ax.get_ylim()[1] / len(nodes)
            y_padding = y_gap / 2
            y = y_padding

            for node in nodes:
                node_circle = plt.Circle(xy = (x, y), radius = 0.5)
                ax.add_patch(node_circle)
                ax.text(x, y, node.name, horizontalalignment = 'center', verticalalignment = 'center')

                node_location_dict[node.name] = (x, y)

                y += y_gap

            x += x_gap

        for connection in self.connections:
            in_pos = node_location_dict[connection.in_node.name]
            out_pos = node_location_dict[connection.out_node.name]

            ax.plot([in_pos[0], out_pos[0]], [in_pos[1], out_pos[1]],
                    color = 'g' if connection.enable else 'r',
                    linestyle = 'solid',
                    alpha = 1,
                    linewidth = 2,
                    zorder = 0)

        return fig
