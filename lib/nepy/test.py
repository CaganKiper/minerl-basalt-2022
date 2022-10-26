import random

from agent import Agent
from population import Population


class TestAgent(Agent):

    def fitness(self):
        fitness = 0
        if self.predict([0, 0])[0] <= 0.1:
            fitness += 1
        if self.predict([0, 1])[0] <= 0.1:
            fitness += 1
        if self.predict([1, 0])[0] <= 0.1:
            fitness += 1
        if self.predict([1, 1])[0] >= 0.9:
            fitness += 1
        return fitness

if __name__ == "__main__":

    pop = Population(TestAgent, 50, 2, 1)
    
    
    for a in pop:
        print(a.fitness)

    
    for i in range(10):
        pop.fit()
    
    pop._agent_list[0]