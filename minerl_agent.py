import abc
import minerl
import gym

from lib.nepy.agent import Agent


class MineRLAgent(Agent):

    def __init__(self):
        self.environment_name = "MineRLObtainDiamondShovel-v0"
        super(MineRLAgent, self).__init__()

    @abc.abstractmethod
    def _env_obs_to_agent(self, minerl_obs):
        pass

    @abc.abstractmethod
    def _agent_action_to_env(self, agent_action):
        pass

    def _act(self, agent_input):
        agent_action = self.phenotype.foward(agent_input)
        return agent_action

    def get_action(self, minerl_obs):
        agent_input = self._env_obs_to_agent(minerl_obs)
        agent_action = self._act(agent_input)
        minerl_action = self._agent_action_to_env(agent_action)
        return minerl_action

    def fitness(self):
        """
            Get Fitness
        """
        env = gym.make(self.environment_name)
        obs = env.reset()

        total_reward = 0
        done = False
        while not done:
            action = self.get_action(obs)
            obs, reward, done, _ = env.step(action)
            total_reward += reward

            env.render()

        return total_reward


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

