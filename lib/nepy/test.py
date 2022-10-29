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

    pop = Population(TestAgent, agent_input_size=2, agent_output_size=1, initial_hidden_size=1, population_size=100)

    for _ in range(25):
        print(f"gen:{pop.generation}")
        print(pop.best_agent.fitness)
        print(pop.average_fitness)
        print()
        pop.fit()

    pop.best_agent.draw().show()