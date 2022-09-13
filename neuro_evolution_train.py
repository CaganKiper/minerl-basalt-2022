from gym import spaces

from lib.nepy.population import Population
from minerl_agent import DiamondAgent

POPULATION_KWARGS = dict(
    population_size = 10,
)

AGENT_KWARGS = dict(

)

TARGET_OBSERVATION_SPACE = {
    "pov": spaces.Box(low = 0, high = 255, shape = (360, 640, 3)),
    "inventory": {
        "oak_wood": spaces.Box(low = 0, high = 2304, shape = ()),
        "oak_plank": spaces.Box(low = 0, high = 2304, shape = ())
    }
}

TARGET_ACTION_SPACE = {
    "camera": spaces.Box(low = -180.0, high = 180.0, shape = (2,)),
    "forward": spaces.Discrete(2),
    "back": spaces.Discrete(2),
    "left": spaces.Discrete(2),
    "right": spaces.Discrete(2),
    "attack": spaces.Discrete(2),
    "jump": spaces.Discrete(2)
}


if __name__ == "__main__":
    print("Initializing Population")
    pop = Population(DiamondAgent, **POPULATION_KWARGS)

    print("Training Population")
    pop.fit()
