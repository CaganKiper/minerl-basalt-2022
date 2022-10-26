import numpy as np
from numpy.random import choice
from agent import Agent
import random


class Population:

    def __init__(self, agent_class, population_size, agent_input_size, agent_output_size):
        self.agent_class = agent_class
        self.population_size = population_size
        self.generation = 0

        self.innovation_table = np.zeros((agent_input_size, agent_input_size), dtype=int)
        self.max_inv_num = 1

        self._agent_list = [agent_class(agent_input_size, agent_output_size, self.get_innovation_number) for i in
                            range(self.population_size)]
        
        self.species_dict = {1:{'id':1, 'member list':[], 'offspring count':0, 
                              'total fitness':0, 'average fitness':0, 
                              'average adjusted fitness:':0,
                              'generation since last improved:':0}}

    def __iter__(self):
        for agent in self._agent_list:
            yield agent


    def fit(self):
        new_population = self._get_next_population()
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
    


    def _get_next_population(self):
        agent_list = self._selection()
        
        return agent_list
    
    #TODO: Beautify
    
    # speciation
    # FIXME: Make threshold a class attribute
    def _speciate(self, *, threshold=4):
        temp_agent_list = self._agent_list.copy()
        species_id = 0
        while temp_agent_list:
            champion = random.choice(temp_agent_list)
            
            species_id += 1
            champion.species_id = species_id
            
            self.species_dict[species_id]['id'] = species_id
            self.species_dict[species_id]['member list'].append(champion)
            self.species_dict[species_id]['total fitness'] += champion.fitness
            temp_agent_list.remove(champion)

            same_specie_list = []
            for agent in temp_agent_list:
                if agent.comparison_check(champion) < threshold:
                    agent.species_id = species_id
                    same_specie_list.append(agent)
                    self.species_dict[species_id]['total fitness'] += agent.fitness
            
            
            self.species_dict[species_id]['member list'] = self.species_dict[species_id]['member list'] + same_specie_list
            member_count= len(self.species_dict[species_id]['member list'])
            
            self.species_dict[species_id]['average fitness'] = (self.species_dict[species_id]['total fitness'] / member_count)  
            total_adjusted_fitness = 0
            for agent in self.species_dict[species_id]['member list']:
                agent.adjusted_fitness = (agent.fitness / member_count)
                total_adjusted_fitness += agent.adjusted_fitness
                
            total_adjusted_fitness += champion.adjusted_fitness
            self.species_dict[species_id]['average adjusted fitness'] = total_adjusted_fitness / member_count
            
            temp_agent_list = [agent for agent in temp_agent_list if agent not in same_specie_list]

        global_total_adjusted_fitness = 0
        for specie in self.species_dict:
            global_total_adjusted_fitness += specie['average adjusted fitness']
        global_average_adjusted_fitness = (global_total_adjusted_fitness / len(self.species_dict))
        for specie in self.species_dict:
            specie['offspring count'] = ((specie['average adjusted fitness']/global_average_adjusted_fitness)*len(specie['member list']))
        
    def _selection(self, survival_threshold = 80):
        new_agents_list = []
        for specie in self.species_dict:
            offspring_list = []
            offspring_num = specie['offspring count']
            
            sorted_agents = sorted(specie['member list'], key=lambda x: x.fitness, reverse=True)
            
            survived_agents = sorted_agents[int(len(sorted_agents) * (survival_threshold/100)):]
            
            fitness_list = []
            for agent in survived_agents:
                fitness_list.append(agent.fitness)
            
            weights = [float(i)/sum(fitness_list) for i in fitness_list]   
            for i in range(offspring_num):
                parents = choice(
                    survived_agents, 2, p=weights)
                #crossover
                offspring_list.append(self._cross_over(parents))
            new_agents_list = new_agents_list + offspring_list
        return new_agents_list 
    def _cross_over(self, parent_list):
        
        if parent_list[0].fitness > parent_list[1].fitness:
            offspring = parent_list[0]
        elif parent_list[1].fitness > parent_list[0].fitness:
            offspring = parent_list[1]
        else:
            offspring = parent_list[0]
        
        # offspring = parent_list[0] if parent_list[0].fitness > parent_list[1].fitness else parent_list[1] if parent_list[1].fitness > parent_list[0].fitness else parent_list[0] 

        inv_list_a = parent_list[0].genome.get_innovation_list()
        inv_list_b = parent_list[1].genome.get_innovation_list()
            
            
        common_inv_list = list(set(inv_list_a).intersection(inv_list_b))   
        
        for inv in common_inv_list:
            conn1 = parent_list[0].genome.find_connection(inv)
            conn2 = parent_list[1].genome.find_connection(inv)

            weight1 = conn1.weight
            weight2 = conn2.weight
            
            num = random.uniform(0, 1)
            if num < 0.5:
                selected_weight = weight1
            else:
                selected_weight = weight2
            
            
            offspring_conn = offspring.genome.find_connection(inv)
            offspring_conn.weight = selected_weight
        
        return offspring
            