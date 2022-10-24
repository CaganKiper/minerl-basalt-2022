import random

from agent import Agent
from population import Population


class TestAgent(Agent):

    def fitness(self):
        return 1


if __name__ == "__main__":

    pop = Population(TestAgent, 10, 2, 2)

    pop._agent_list[0].genome.connections.pop(0)
    pop._agent_list[0].genome.connections.pop(1)

    for a in pop:
        for connection in a.genome.connections:
            connection.weight = random.uniform(0, 1)

        print(a.genome)


    pop._speciate(threshold = 0.20)

    for agent in pop:
        print(agent.species_id)
