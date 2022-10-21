from matplotlib import pyplot as plt

from network.node import Node
from network.connection import Connection
import random

class Genome:

    def __init__(self, sensor_size, actuator_size, innovation_method):
        self.sensor_size = sensor_size
        self.actuator_size = actuator_size
        self.nodes = []
        self.connections = []

        self.species_id = None

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
                        self.connections.append(Connection(node_in, node_out, innovation_number = innovation_method(node_in.name, node_out.name)))
        # ================================ #

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

    def add_connection(self):
        pass

    def mutate(self):
        pass

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
    
    def get_conn_by_inv_num(self, innovation_number):
        connection_list = self.connections
        for conn in connection_list:
            if conn.innovation_number == innovation_number:
                connection = conn
                break
        return connection

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
