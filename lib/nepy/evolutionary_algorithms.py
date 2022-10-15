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
    g1 = Genome(3, 3)
    for con in g1.connections:
        if random.random() < 0.1:
            con.enable = False

        con.weight = random.random()

    g1.draw_network().show()
    prediction = g1.foward([0.8, 0.6, 0.2])

    print(prediction)
