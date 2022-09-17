import random


class Connection:
    def __init__(self, in_node, out_node, weight=0, enable=True, innovation_number=None):
        self.in_node = in_node
        self.out_node = out_node

        self.weight = random.uniform(0, 1)
        self.enable = enable

        self.innovation_number = innovation_number

    def __str__(self):
        return f"Connection({'ENABLED' if self.enable else 'DISABLED'}): " \
               f"inv:[{self.innovation_number}] {self.in_node} --[{self.weight:.3f}]--> {self.out_node} "

    def __repr__(self):
        return self.__str__()

