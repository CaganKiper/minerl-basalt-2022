import math
from enum import Enum


class NodeType(Enum):
    SENSOR = 0
    ACTUATOR = 1
    HIDDEN = 2
    BIAS = 3


class Node:
    def __init__(self, node_id: int, node_type: NodeType, layer=None):
        self.node_id = node_id
        self.node_type = node_type  # FIXME: Rename element  # type 0=Sensor, 1=Actuator, 2=Hidden, 3=Bias

        self.layer = layer
        self.input = None
        self.output = None

    def __str__(self):
        return f"({self.node_id})"

    def __repr__(self):
        return f"({self.node_id})"

    def activate(self):
        if self.node_type == NodeType.SENSOR or self.node_type == NodeType.BIAS:
            self.output = self.input
        else:
            self.output = self.activision_function(self.input)

    def activision_function(self, x):
        return sigmoid(x)


def sigmoid(x):
    return 1 / (1 + math.exp(-x))
