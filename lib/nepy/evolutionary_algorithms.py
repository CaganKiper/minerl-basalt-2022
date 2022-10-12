import random

from lib.nepy.genome import Genome
from lib.nepy.network.connection import Connection
from lib.nepy.network.node import Node
from lib.nepy.agent import Agent


def selection(population, *, selection_size=2):
    """
    TODO:
        args:
            population: Population object
            selection_size: number of agents to be selected (default=2)
        kwargs:
            TBD
        return: returns a List of selected Agents
    """
    parent_list = random.sample(population, selection_size)
    return parent_list


def cross_over(agent_list):
    """
    TODO:
        args:
            agent_list: list of parents
        kwargs:
            TBD
        return: returns a new Agent derived from each agent from agent_list
    """
    
    if agent_list[0].fitness > agent_list[1].fitness:
        child_genome = _cross_over_genome(agent_list[0].genotype, agent_list[1].genotype)
        
    elif agent_list[1].fitness > agent_list[0].fitness:
        child_genome = _cross_over_genome(agent_list[1].genotype, agent_list[0].genotype)
        
    else:
        child_genome = __cross_over_genome_same_fitness(agent_list[0].genotype, agent_list[1].genotype)
        
    child = Agent(child_genome)
    
    return child


def _cross_over_genome(genotype_1, genotype_2):
    temp = []
    for connection in genotype_1:
        inv = connection.innovation_number
        if genotype_2[inv] is not None:
            # random choice
            temp.append(random.choice([connection, genotype_2[inv]]))
        else:
            temp.append(connection)

    return Genome(temp)


def __cross_over_genome_same_fitness(genotype_1, genotype_2):
    # TODO: Performance check

    temp = {}
    for connection in genotype_1:
        inv = connection.innovation_number

        if genotype_2[inv] is not None:
            random.choice([connection, genotype_2[connection.innovation_number]])
        else:
            temp[inv] = connection

    for connection in genotype_2:
        inv = connection.innovation_number

        if not (inv in temp.keys()):
            temp[inv] = connection

    return Genome(temp.values())


def mutation(agent, *, mutation_rate=0.02):
    """
    TODO:
        args:
            agent: agent to mutate
        kwargs:
            mutation_rate: probability of a mutation occurring (input as percent_rate/100 ex. 0.2 = %20, 0.03 = %3 ...)(default=0.02 = %2)
        return: returns the mutated input agent
    """
    return agent


if __name__ == "__main__":
    n1 = Node("1", "Input")
    n2 = Node("2", "Input")
    n3 = Node("3", "Input")
    n4 = Node("4", "Output")

    n5 = Node("5")
    n6 = Node("6")

    g1_connection_genes = [
        Connection(n1, n4, innovation_number = 1),
        Connection(n2, n4, enable = False, innovation_number = 2),
        Connection(n3, n4, innovation_number = 3),
        Connection(n2, n5, innovation_number = 4),
        Connection(n5, n4, innovation_number = 5),
        Connection(n1, n5, innovation_number = 8),
    ]

    g2_connection_genes = [
        Connection(n1, n4, innovation_number = 1),
        Connection(n2, n4, enable = False, innovation_number = 2),
        Connection(n3, n4, innovation_number = 3),
        Connection(n2, n5, innovation_number = 4),
        Connection(n5, n4, enable = False, innovation_number = 5),
        Connection(n5, n6, innovation_number = 6),
        Connection(n6, n4, innovation_number = 7),
        Connection(n3, n5, innovation_number = 9),
        Connection(n1, n6, innovation_number = 10)
    ]

    g1 = Genome(g1_connection_genes)
    g2 = Genome(g2_connection_genes)

    g3 = _cross_over_genome(g1, g2)

    print(g3)

