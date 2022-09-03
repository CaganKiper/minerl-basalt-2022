import abc

from lib.nepy.agent import Agent


class MineRLAgent(Agent):

    @abc.abstractmethod
    def _env_obs_to_agent(self, minerl_obs):
        pass

    @abc.abstractmethod
    def _agent_action_to_env(self, agent_action):
        pass

    def _act(self, agent_input):
        agent_action = agent_input
        return agent_action

    def get_action(self, minerl_obs):
        agent_input = self._env_obs_to_agent(minerl_obs)
        agent_action = self._act(agent_input)
        minerl_action = self._agent_action_to_env(agent_action)
        return minerl_action

    def fitness(self):
        raise NotImplementedError


class DiamondAgent(MineRLAgent):

    def _env_obs_to_agent(self, minerl_obs):
        """
            TODO: Implement it
        """
        pass

    def _agent_action_to_env(self, agent_action):
        """
            TODO: Implement it
        """
        pass

