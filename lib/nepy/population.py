import numpy as np

from agent import Agent
import random


class Population:

    def __init__(self, agent_class, population_size, agent_input_size, agent_output_size):
        self.agent_class = agent_class
        self.population_size = population_size
        self.generation = 0

        self.innovation_table = np.zeros((agent_input_size, agent_input_size))
        self.max_inv_num = 1

        self._agent_list = [agent_class(agent_input_size, agent_output_size, self.get_innovation_number) for i in range(self.population_size)]

    def __iter__(self):
        for agent in self._agent_list:
            yield agent

    def fit(self):
        new_population = self._get_new_population()
        self._agent_list = new_population

        self.generation += 1

        return self

    def get_innovation_number(self, in_name, out_name):
        if self.innovation_table.shape[0] - 1 >= in_name and self.innovation_table.shape[1] - 1 >= out_name:
            if self.innovation_table[in_name, out_name] == 0:
                self.innovation_table[in_name, out_name] = self.max_inv_num
                self.max_inv_num += 1

            return self.innovation_table[in_name, out_name]

        else:
            self.innovation_table = np.pad(self.innovation_table, ((0, 1), (0, 1)), "constant", constant_values = 0)
            return self.get_innovation_number(in_name, out_name)

    def _get_new_agent(self):
        return self

    def _get_new_population(self):
        new_population = []

        while len(new_population) < self.population_size:
            new_population.append(self._get_new_agent())

        return new_population
#speciation
    def _speciate(self, threshold=4):
        temp_agent_list = self._agent_list.copy()
        species_id = 0
        while temp_agent_list:
            champion = random.choice(temp_agent_list)

            species_id += 1
            champion.species_id = species_id

            temp_agent_list.remove(champion)

            for agent in temp_agent_list:
                if agent.comparison_check(champion) < threshold:
                    agent.species_id = species_id
                    temp_agent_list.remove(agent)
