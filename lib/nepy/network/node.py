class Node:
    def __init__(self, node_name=None, node_type="Hidden"):
        self.node_name = node_name
        self.type = node_type

    def __str__(self):
        return f"({self.node_name})"
