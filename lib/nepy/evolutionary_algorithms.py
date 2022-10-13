import random

from genome import Genome
from network.connection import Connection
from network.node import Node
from agent import Agent


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
    g1 = Genome(2, 2)
    c1 = Connection(g1.nodes[0],g1.nodes[-1],innovation_number=1)
    c2 = Connection(g1.nodes[1],g1.nodes[-1],innovation_number=2)
    c3 = Connection(g1.nodes[2],g1.nodes[-1],innovation_number=3)
    c4 = Connection(g1.nodes[0],g1.nodes[-2],innovation_number=4)
    c5 = Connection(g1.nodes[1],g1.nodes[-2],innovation_number=5)
    c6 = Connection(g1.nodes[2],g1.nodes[-2],innovation_number=6)
    
    g1.connections.append(c1)
    g1.connections.append(c2)
    g1.connections.append(c3)
    g1.connections.append(c4)
    g1.connections.append(c5)
    g1.connections.append(c6)
    
    
    inputs =[1,2]
    g1._load_inputs(inputs)
    
    g1.nodes[3].output = 0.9
    g1.nodes[4].output = 0.1
    print(g1._get_outputs())
    g1.draw_network()
    
    
    
    
    
