import abc
import minerl
import gym

from lib.nepy.agent import Agent


class MineRLAgent(Agent):

    def __init__(self):
        super(MineRLAgent, self).__init__()

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

        env.close()
        return total_reward


class DiamondAgent(MineRLAgent):

    def __init__(self):
        self.environment_name = "MineRLObtainDiamondShovel-v0"
        self.target_observation_space = None
        self.target_action_space = None
        self.selected_inventory_items = ["diamond", "oak_log", "oak_planks", "oak_wood", "dark_oak_log",
                                         "dark_oak_planks", "dark_oak_wood", "wooden_axe", "wooden_pickaxe",
                                         "stone_axe", "stone_pickaxe", "stick", "cobblestone"]

        super(DiamondAgent, self).__init__()

    def _filter_inventory_items(self, minerl_obs):
        return list(set(list(minerl_obs["inventory"].keys())).intersection(self.selected_inventory_items))

    def _process_pov(self, minerl_obs):
        return minerl_obs["pov"]

    def _process_inventory(self, minerl_obs):
        filtered_items = self._filter_inventory_items(minerl_obs)
        print(dict(
            zip(
                filtered_items,
                [minerl_obs["inventory"][value] for value in filtered_items]
            ))
        )
        return list(minerl_obs["inventory"].values())

    def _env_obs_to_agent(self, minerl_obs):
        return [self._process_pov(minerl_obs), self._process_inventory(minerl_obs)]

    def _process_camera(self, values):
        return tuple(map(lambda x: round(x), (-180 + (180 - -180) * v for v in values)))

    def _agent_action_to_env(self, agent_action):
        return ({"camera": self._process_camera(agent_action[:2])} |
                dict(
                    zip(agent_action.keys(), list((map(lambda x: 0 if x < 0.5 else 1, agent_action[2:]))))
                ))
