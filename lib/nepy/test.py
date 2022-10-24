from agent import Agent
from population import Population


class TestAgent(Agent):

    def fitness(self):
        return 1


if __name__ == "__main__":

    pop = Population(TestAgent, 10, 2, 2)

    for a in pop:
        print(a.genome)

    pop._speciate(threshold = 100000)

    for agent in pop:
        print(agent.species_id)
