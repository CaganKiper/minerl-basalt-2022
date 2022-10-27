import random

from agent import Agent
from population import Population


class TestAgent(Agent):

    def fitness(self):
        fitness = 0

        fitness += (1 - (self.predict([0, 0])[0]))
        fitness += self.predict([0, 1])[0]
        fitness += self.predict([1, 0])[0]
        fitness += (1 - (self.predict([1, 1])[0]))

        return fitness

if __name__ == "__main__":

    pop = Population(TestAgent, 3, 2, 1)
    
    for a in pop:
        print(f"{a.fitness:.2f}")
        
    
    for i in range(10):
        pop.fit()
    
    for a in pop:
        print(f"{a.fitness:.2f}")
    