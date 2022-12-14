import abc

from lib.nepy.phenotype import Phenotype


class Agent(abc.ABC):

    def __init__(self):
        self.phenotype = Phenotype()

        self.fitness = self.fitness()

    @abc.abstractmethod
    def fitness(self):
        pass

    def predict(self, agent_input):
        return self.phenotype.forward(agent_input)
