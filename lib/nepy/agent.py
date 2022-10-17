import abc
from lib.nepy.genome import Genome


class Agent(abc.ABC):
    def __init__(self, input_size, output_size):
        self.genome = Genome(input_size, output_size)
        self.fitness = self.fitness()

    @property
    def species_id(self):
        return self.genome.species_id

    @species_id.setter
    def species_id(self, value):
        self.genome.species_id = value

    @abc.abstractmethod
    def fitness(self):
        pass

    def predict(self, agent_input):
        return self.genome.forward(agent_input)
