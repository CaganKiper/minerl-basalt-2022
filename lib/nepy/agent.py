import abc

from genome import Genome


class Agent(abc.ABC):
    def __init__(self, input_size, output_size, innovation_method):
        self.genome = Genome(input_size, output_size, innovation_method)
        self.fitness = self.fitness()
        self.adjusted_fitness = 0

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

        inv_list_a = self.genome.get_innovation_list()
        inv_list_b = agent_to_compare.genome.get_innovation_list()

        # excess
        if max(inv_list_a) < max(inv_list_b):
            for inv in inv_list_b:
                if inv > inv_list_a:
                    excess_genes += 1
        elif max(inv_list_b) < max(inv_list_a):
            for inv in inv_list_a:
                if inv > inv_list_b:
                    excess_genes += 1

        # disjoint
        common_inv_list = list(set(inv_list_a).intersection(inv_list_b))

        disjoint_a = len(inv_list_a) - len(common_inv_list)
        disjoint_b = len(inv_list_b) - len(common_inv_list)
        disjoint_genes = (disjoint_a + disjoint_b - excess_genes)

        # weight difference
        total_diff = 0
        for inv in common_inv_list:
            conn1 = self.genome.find_connection(inv)
            conn2 = agent_to_compare.genome.find_connection(inv)

            weight1 = conn1.weight
            weight2 = conn2.weight

            total_diff += abs(weight1 - weight2)

        weight_diff = (total_diff / len(common_inv_list))

        n = 1
        if normalized:
            if len(self.genome.connections) >= len(agent_to_compare.genome.connections):
                n = len(self.genome.connections)
            else:
                n = len(agent_to_compare.genome.connections)

        compatibility_difference = abs((c1 * (excess_genes / n))
                                       + (c2 * (disjoint_genes / n))
                                       + (c3 * weight_diff))

        return compatibility_difference
    
    def draw(self):
        return self.genome.draw_network()
