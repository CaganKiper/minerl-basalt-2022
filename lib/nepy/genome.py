from network.node import Node
from network.connection import Connection

import graphviz

class Genome:

    def __init__(self, sensor_size, actuator_size):
        self.nodes = []
        self.connections = []

        self.largest_node_id = 0
        # ========== NODES LIST ========== #
        for _ in range(sensor_size):  # Sensor nodes
            self.nodes.append(self.get_new_node(node_type = 0))

        self.nodes.append(self.get_new_node(node_type = 3))  # Bias node in the input layer

        for _ in range(actuator_size):  # Actuator nodes
            self.nodes.append(self.get_new_node(node_type = 1))
        # ================================ #

        # ======= CONNECTIONS LIST ======= #

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

    def _load_inputs(self, inputs):
        nodes = self.nodes
        for count, input in enumerate(inputs): 
            nodes[count].input = input
            

    def foward(self):
        pass

    def get_new_node(self, node_type):
        self.largest_node_id += 1
        return Node(self.largest_node_id, node_type)

    def draw_network(self):
        nodes = self.nodes
        node_names =[]
        for node in nodes:
            node_names.append(node.name)
        connections = self.connections
# =============================================================================
#         layer_dict = {}
#         for node in self.nodes:
#             layer = node.layer
#             if layer in layer_dict.keys():
#                 layer_dict[layer] += 1
#             else:
#                 layer_dict[layer] = 1
# =============================================================================
        
        node_attrs = {
        'shape': 'circle',
        'fontsize': '9',
        'height': '0.2',
        'width': '0.2'}

        dot = graphviz.Digraph(format='png', node_attr=node_attrs)
        
        for connect_gene in connections:
            if connect_gene.enable == True:
                input = str(connect_gene.in_node.name)
                output = str(connect_gene.out_node.name)
    
                style = 'solid' if connect_gene.enable == True else 'dotted'
                color = 'green' if float(connect_gene.weight) > 0 else 'red'
                width = str(0.1 + abs(float(connect_gene.weight / 5.0)))
                dot.edge(input, output, _attributes={'style': style, 'color': color, 'penwidth': width})

        dot.render("trial_network", view=True)

        return dot
        
        
