import abc
from lib.nepy.genome import Genome


class Agent(abc.ABC):
    def __init__(self, input_size, output_size, innovation_method):
        self.genome = Genome(input_size, output_size, innovation_method)
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

    def comparison_check(self, agent_to_compare, c1=1, c2=1, c3=0.4, normalized=True):

        excess_genes = 0
        disjoint_genes = 0
        weight_diff = 0
        
        # TODO: Beautify
        
        inv_list_a = []
        inv_list_b = []
        
        for conn in self.genome.connections:
            inv_list_a.append(conn.innovation_number)
            
        for conn in agent_to_compare.genome.connections:
            inv_list_b.append(conn.innovation_number)
        
        #excess
        if max(inv_list_a) < max(inv_list_b):
            for inv in inv_list_b:
                if inv > inv_list_a:
                    excess_genes += 1
        elif max(inv_list_b) < max(inv_list_a):
            for inv in inv_list_a:
                if inv > inv_list_b:
                    excess_genes += 1
            
        n = 1
        if normalized:
            if len(self.genome.connections) >= len(agent_to_compare.genome.connections):
                n = len(self.genome.connections)
            else:
                n = len(agent_to_compare.genome.connections)

        for connection in self.genome.connections:
            if connection.enable:
                print("a")

        compatibility_difference = abs((c1 * (excess_genes / n))
                                       + (c2 * (disjoint_genes / n))
                                       + (c3 * weight_diff))

        return compatibility_difference
