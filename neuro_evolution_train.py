from lib.nepy.population import Population
from minerl_agent import DiamondAgent

POPULATION_KWARGS = dict(
    population_size = 10,
)

AGENT_KWARGS = dict(

)

TARGET_OBSERVATION_SPACE = dict(
    pov = [360, 640],
    inventory = {
        "oak_wood"
    }
)

TARGET_ACTION_SPACE = dict(

)

if __name__ == "__main__":
    print("Initializing Population")
    pop = Population(DiamondAgent, **POPULATION_KWARGS)

    print("Training Population")
    pop.fit()
