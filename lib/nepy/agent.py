import abc

from lib.nepy.phenotype import Phenotype


class Agent(abc.ABC):

    def __init__(self):
        self.phenotype = Phenotype()

    @abc.abstractmethod
    def fitness(self):
        pass