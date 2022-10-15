import math


class Node:
    def __init__(self, name, type_, layer=None):
        self.name = name
        self.type_ = type_  # FIXME: Rename element  # type 0=Sensor, 1=Actuator, 2=Hidden, 3=Bias

        self.layer = layer
        self.input = None
        self.output = None

    def __str__(self):
        return f"({self.name})"

    def __repr__(self):
        return f"({self.name})"

    def activate(self):
        if self.type_ == 0 or self.type_ == 3:
            self.output = self.input
        else:
            self.output = self.activision_function(self.input)

    def activision_function(self, x):
        return sigmoid(x)


def sigmoid(x):
    return 1 / (1 + math.exp(-x))
