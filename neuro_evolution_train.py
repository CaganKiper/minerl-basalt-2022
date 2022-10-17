from lib.nepy.population import Population
from minerl_agent import DiamondAgent

POPULATION_KWARGS = dict(
    population_size = 10,
    agent_input_size = 5,
    agent_output_size = 4
)

if __name__ == "__main__":
    print("Initializing Population")
    pop = Population(DiamondAgent, **POPULATION_KWARGS)

    print("Training Population")
    pop.fit()
