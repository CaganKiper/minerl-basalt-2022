from matplotlib import pyplot as plt

from lib.nepy.network.node import Node
from lib.nepy.network.connection import Connection

class Genome:

    def __init__(self, sensor_size, actuator_size):
        self.sensor_size = sensor_size
        self.actuator_size = actuator_size
        self.nodes = []
        self.connections = []

        self.largest_node_id = 0
        # ========== NODES LIST ========== #
        for _ in range(sensor_size):  # Sensor nodes
            self.nodes.append(self.get_new_node(node_type = 0, layer=1))

        self.nodes.append(self.get_new_node(node_type = 3, layer=1))  # Bias node in the input layer

        for _ in range(actuator_size):  # Actuator nodes
            self.nodes.append(self.get_new_node(node_type = 1, layer=3))
        # ================================ #

        # ======= CONNECTIONS LIST ======= #
        for node_out in self.nodes:
            if node_out.type_ == 1:
                for node_in in self.nodes:
                    if node_in.type_ == 0 or node_in.type_ == 3:
                        self.connections.append(Connection(node_in, node_out))
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

    def _get_outputs(self):
        nodes = self.nodes
        outputs = []
        start = self.sensor_size + 1
        end = start + self.actuator_size
        for outnode in nodes[start:end]:
            outputs.append(outnode.output)

        return outputs

    def foward(self):
        pass

    def get_new_node(self, node_type, layer=None):
        self.largest_node_id += 1
        return Node(self.largest_node_id, node_type, layer=layer)

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

                node_location_dict[node.name] = (x, y)

                y += y_gap

            x += x_gap

        for connection in self.connections:
            in_pos = node_location_dict[connection.in_node.name]
            out_pos = node_location_dict[connection.out_node.name]

            ax.plot([in_pos[0], out_pos[0]], [in_pos[1], out_pos[1]],
                    color='g' if connection.enable else 'r',
                    linestyle='solid' if connection.enable else 'dashed',
                    alpha=connection.weight if not connection.enable else 1,
                    linewidth=1 + connection.weight,
                    zorder=0)

        return fig
