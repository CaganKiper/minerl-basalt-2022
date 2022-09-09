from lib.nepy.population import Population
from minerl_agent import DiamondAgent

POPULATION_KWARGS = dict(
    population_size = 10,
)

AGENT_KWARGS = dict(

)

if __name__ == "__main__":
    print("Initializing Population")
    pop = Population(DiamondAgent, **POPULATION_KWARGS)

    print("Training Population")
    pop.fit()
