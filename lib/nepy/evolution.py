from lib.nepy.agent import Agent


def selection(self, selection_size=2):
    """
    TODO:  args:
              selection_size: number of agents to be selected (default=2)
          kwargs:
              TBD
          return: returns a List of selected Agents
    """
    return list()


def cross_over(agent_list):
    """
    TODO:  args:
              agent_list: list of parents
          kwargs:
              TBD
          return: returns a new Agent derived from each agent from agent_list
    """
    return Agent()


def mutate(agent, *, mutation_rate=0.02):
    """
    TODO:
        args:
            agent: agent to mutate
        kwargs:
            mutation_rate: probability of a mutation occurring (input as percent_rate/100 ex. 0.2 = %20, 0.03 = %3 ...)(default=0.02 = %2)
            return: returns the mutated input agent
    """
    return agent
