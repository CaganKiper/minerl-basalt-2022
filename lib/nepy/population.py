from lib.nepy.agent import Agent
from lib.nepy.evolutionary_algorithms import selection, cross_over, mutation


class Population:

    def __init__(self, agent_class, population_size):
        self.agent_class = agent_class
        self.population_size = population_size
        self.generation = 0

        self._agent_list = [agent_class() for i in range(self.population_size)]

        self.innovation_table = []

    def __iter__(self):
        for agent in self._agent_list:
            yield agent

    def fit(self):
        new_population = self._get_new_population()
        self._agent_list = new_population

        self.generation += 1

        return self

    def _get_new_agent(self):
        return mutation(cross_over(selection(self)))

    def _get_new_population(self):
        new_population = []

        while len(new_population) < self.population_size:
            new_population.append(self._get_new_agent())

        return new_population
