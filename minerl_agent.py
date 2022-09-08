import abc

import gym

from lib.nepy.agent import Agent


class MineRLAgent(Agent):

    def __init__(self, environment_name="MineRLObtainDiamondShovel-v0"):
        super(MineRLAgent, self).__init__()
        self.environment_name = environment_name

    @abc.abstractmethod
    def _env_obs_to_agent(self, minerl_obs):
        pass

    @abc.abstractmethod
    def _agent_action_to_env(self, agent_action):
        pass

    def _act(self, agent_input):
        agent_action = self.predict(agent_input)
        return agent_action

    def get_action(self, minerl_obs):
        agent_input = self._env_obs_to_agent(minerl_obs)
        agent_action = self._act(agent_input)
        minerl_action = self._agent_action_to_env(agent_action)
        return minerl_action

    def fitness(self):
        print("F")
        env = gym.make(self.environment_name)
        obs = env.reset()

        done = False
        while not done:
            print(obs)

            agent_action = self._env_obs_to_agent(obs)
            env_action = self._agent_action_to_env(agent_action)

            obs, reward, done, _ = env.step(env_action)

            env.render()

        return 0


class DiamondAgent(MineRLAgent):

    def __init__(self):
        super(DiamondAgent, self).__init__()
        
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
