from lib.nepy.network.node import Node
from lib.nepy.network.connection import Connection


class Genome:

    def __init__(self, sensor_size, actuator_size):
        self.nodes = []
        self.connections = []

        # ========== NODES LİST ========== #
        for _ in range(sensor_size):  # Sensor nodes
            self.nodes.append(self.get_new_node(node_type = 0))

        self.nodes.append(self.get_new_node(node_type = 3))  # Bias node in the input layer

        for _ in range(actuator_size):  # Actuator nodes
            self.nodes.append(self.get_new_node(node_type = 1))
        # ================================ #

        # ======= CONNECTIONS LIST ======= #

        # ================================ #
        self.largest_node_id = 1

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
        pass

    def foward(self):
        pass

    def get_new_node(self, node_type):
        self.largest_node_id += 1
        return Node(self.largest_node_id, node_type)

    def test(self):
        nonlocal innovation_table
