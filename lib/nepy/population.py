from lib.nepy.agent import Agent
import random


class Population:

    def __init__(self, agent_class, population_size, agent_input_size, agent_output_size):
        self.agent_class = agent_class
        self.population_size = population_size
        self.generation = 0

        self._agent_list = [agent_class(agent_input_size, agent_output_size) for i in range(self.population_size)]

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
        return self

    def _get_new_population(self):
        new_population = []

        while len(new_population) < self.population_size:
            new_population.append(self._get_new_agent())

        return new_population
    
    def _speciate(self, threshold = 4):
        temp_agent_list = self.agentlist
        species_id = 0
        while temp_agent_list:
            new_specie = random.choise(temp_agent_list)
            
            species_id += 1
            new_specie.species_id = species_id
            
            temp_agent_list.remove(new_specie)
            
            for specie in temp_agent_list:
                
                if  _compatibility_difference(new_specie,specie) < threshold:
                    specie.species_id = species_id
                    temp_agent_list.remove(specie)
                    
                    
        