from lib.nepy.agent import Agent


class Population:

    def __init__(self, agent, *, population_size):
        self.agent = agent
        self.size = population_size

        print(agent)
        print(type(agent))
        print(agent())

