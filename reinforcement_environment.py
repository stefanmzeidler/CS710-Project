from __future__ import absolute_import, division, print_function

import os
from collections import defaultdict

import numpy as np
import reverb
import tensorflow as tf
from tf_agents.agents.dqn import dqn_agent
from tf_agents.bandits.agents import lin_ucb_agent
from tf_agents.drivers import py_driver
from tf_agents.environments import tf_py_environment as tfpy
from tf_agents.environments.py_environment import PyEnvironment
from tf_agents.networks import sequential
from tf_agents.policies import policy_saver
from tf_agents.policies import py_tf_eager_policy
from tf_agents.policies import random_tf_policy
from tf_agents.policies import tf_py_policy
from tf_agents.replay_buffers import reverb_replay_buffer
from tf_agents.replay_buffers import reverb_utils
from tf_agents.specs import ArraySpec
from tf_agents.specs import array_spec
from tf_agents.specs import tensor_spec
from tf_agents.trajectories import time_step as ts
from tf_agents.utils import common


from card import Card
from game_manager import Game
from game_utils import score_round
from player import Player
from random_player import RandomPlayer


class SushiGoRLEnvironment(PyEnvironment, Player):
    CATEGORIES = [Card.DOUBLE_MAKI, Card.DUMPLING, Card.EGG, Card.PUDDING, Card.SALMON, Card.SASHIMI,
                  Card.SINGLE_MAKI, Card.SQUID, Card.TEMPURA, Card.TRIPLE_MAKI, Card.WASABI]

    def __init__(self):
        super().__init__()
        self.name = 'RLPlayer'
        players = [self, RandomPlayer("Random1"), RandomPlayer("Random2")]
        self.game = Game(players)

        self._action_spec = tensor_spec.BoundedTensorSpec(
            shape=(), dtype=np.int32, minimum=0, maximum=len(SushiGoRLEnvironment.CATEGORIES) - 1, name='action')
        self._observation_spec = {
            'observation': array_spec.BoundedArraySpec(shape=(len(SushiGoRLEnvironment.CATEGORIES),), minimum=0,
                                                       maximum=len(SushiGoRLEnvironment.CATEGORIES) - 1, dtype=np.int32,
                                                       name='observation'),
            'mask': ArraySpec(shape=(len(SushiGoRLEnvironment.CATEGORIES),), dtype=bool, name='mask'), }
        # self._reward_spec = tensor_spec.BoundedTensorSpec(shape=(), dtype=np.int32, minimum=0, maximum = 1000,  name='reward')
        self._state = np.zeros(len(SushiGoRLEnvironment.CATEGORIES), dtype=np.int32)
        self._episode_ended = False
        self.card_to_choose = None
        self.qnet = None
        self.agent = None

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def rl_reward(self):
        if len(self.chosen_cards) < self.game.number_cards:
            return 0
        else:
            return self.score

    def _step(self, action) -> ts.TimeStep:
        self.card_to_choose = Card(SushiGoRLEnvironment.CATEGORIES[action])
        # names = [hand_card.name for hand_card in self.hand]
        # print(names)
        # print(action)
        # assert self.card_to_choose.name in names
        if self._episode_ended:
            return self.reset()
        elif self.game.game_round > 3 or self.play_single_turn() is None:
            self._episode_ended = True
        observation = {'observation': self._state, 'mask': self.hand_to_action_mask(self.hand)}
        if self._episode_ended:
            reward = self.score
            return ts.termination(observation=observation, reward=reward)
        else:
            return ts.transition(observation=observation, reward=0, discount=1.0)

    @staticmethod
    def observation_and_action_constraint_splitter(observation):
        return observation['observation'], observation['mask']

    def play_single_turn(self):
        if self.game.turn > self.game.number_cards:
            self.game.game_round += 1
            if self.game.game_round > Game.TOTAL_ROUNDS:
                return None
            self.game.turn = 0
            score_round(self.game.players)
            for player in self.game.players:
                player.card_history[self.game.game_round] = player.chosen_cards
        if self.game.turn == 0 and len(self.hand) == 0:
            self.game.deal_cards()
        for player in self.game.players:
            player.play_turn(self.game.get_game_state())
        self.game.pass_hands()
        self.game.turn += 1
        self._state = self.cards_to_vector(self.chosen_cards)

    def _reset(self) -> ts.TimeStep:
        self.hand = []
        self.card_history = defaultdict(list)
        self.chosen_cards = []
        self.maki_icons = 0
        self.pudding_cards = 0
        self.score = 0
        self.last_played = None
        self._episode_ended = False
        self._state = self.cards_to_vector(self.chosen_cards)
        players = [self, RandomPlayer("Random1"), RandomPlayer("Random1")]
        self.game = Game(players)
        self.game.deal_cards()
        observation = {'observation': self._state, 'mask': self.hand_to_action_mask(self.hand)}
        return ts.restart(observation=observation)

    @staticmethod
    def cards_to_vector(card_list):
        card_names = [c.name for c in card_list]
        vector = np.zeros(len(SushiGoRLEnvironment.CATEGORIES), dtype=np.int32)
        for name in card_names:
            vector[SushiGoRLEnvironment.CATEGORIES.index(name)] += 1
        return np.array(vector, dtype=np.int32)

    @staticmethod
    def hand_to_action_mask(hand):
        card_types = [hand_card.name for hand_card in hand]
        return np.array([card_type in card_types for card_type in SushiGoRLEnvironment.CATEGORIES], dtype=bool)

    def choose_card(self, game_state):
        return self.card_to_choose

    def create_qnet(self, fc_layer_params):
        """
        Adapted from https://github.com/tensorflow/agents/blob/master/docs/tutorials/1_dqn_tutorial.ipynb
        :return:
        """
        # fc_layer_params = (100, 100, 100)
        action_tensor_spec = tensor_spec.from_spec(self.action_spec())
        num_actions = action_tensor_spec.maximum - action_tensor_spec.minimum + 1

        def dense_layer(num_units):
            return tf.keras.layers.Dense(
                num_units,
                activation= tf.keras.activations.relu, #Alternatives: tf.keras.layers.LeakyReLU(alpha=0.01), tf.keras.activations.sigmoid
                kernel_initializer=tf.keras.initializers.VarianceScaling(
                    scale=2.0, mode='fan_in', distribution='truncated_normal'))

        dense_layers = [dense_layer(num_units) for num_units in fc_layer_params]
        q_values_layer = tf.keras.layers.Dense(
            num_actions,
            activation=None,
            kernel_initializer=tf.keras.initializers.RandomUniform(
                minval=-0.03, maxval=0.03),
            bias_initializer=tf.keras.initializers.Constant(-0.2))
        return sequential.Sequential(dense_layers + [q_values_layer])

    def create_agent(self, agent_type, network, learning_rate, loss_fn):
        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        train_step_counter = tf.Variable(0)
        agent_tf_env = tfpy.TFPyEnvironment(self)
        agent = None
        if agent_type is dqn_agent.DqnAgent:
            agent = dqn_agent.DqnAgent(
                time_step_spec = agent_tf_env.time_step_spec(),
                action_spec = agent_tf_env.action_spec(),
                q_network=network,
                optimizer=optimizer,
                td_errors_loss_fn=loss_fn,  # From tutorial original : common.element_wise_squared_loss
                train_step_counter=train_step_counter,
                observation_and_action_constraint_splitter=self.observation_and_action_constraint_splitter)
        elif agent_type is lin_ucb_agent.LinearUCBAgent:
            agent = lin_ucb_agent.LinearUCBAgent(
                time_step_spec = agent_tf_env.time_step_spec(),
                action_spec = agent_tf_env.action_spec()
            )

        agent.initialize()
        return agent

    def compute_avg_return(self, policy, num_episodes=10):
        """
        Adapted from https://github.com/tensorflow/agents/blob/master/docs/tutorials/1_dqn_tutorial.ipynb
        :param policy:
        :param num_episodes:
        :return:
        """
        total_return = 0.0
        for _ in range(num_episodes):
            time_step = self.reset()
            episode_return = 0.0
            while not time_step.is_last():
                action_step = policy.action(time_step)
                time_step = self.step(action_step.action)
                episode_return += time_step.reward
            total_return += episode_return
        avg_return = total_return / num_episodes
        return avg_return.numpy()[0]

    def create_observer(self):
        replay_buffer_max_length = 100000
        table_name = 'uniform_table'
        replay_buffer_signature = tensor_spec.from_spec(
            self.agent.collect_data_spec)
        replay_buffer_signature = tensor_spec.add_outer_dim(
            replay_buffer_signature)

        table = reverb.Table(
            table_name,
            max_size=replay_buffer_max_length,
            sampler=reverb.selectors.Uniform(),
            remover=reverb.selectors.Fifo(),
            rate_limiter=reverb.rate_limiters.MinSize(1),
            signature=replay_buffer_signature)

        reverb_server = reverb.Server([table])

        replay_buffer = reverb_replay_buffer.ReverbReplayBuffer(
            self.agent.collect_data_spec,
            table_name=table_name,
            sequence_length=2,
            local_server=reverb_server)

        rb_observer = reverb_utils.ReverbAddTrajectoryObserver(
            replay_buffer.py_client,
            table_name,
            sequence_length=2)

        return rb_observer

    def train(self, policy_name, agent_type, fc_layer_params  = (100, 50), num_eval_episodes=10, initial_collect_steps=100, batch_size=64, learning_rate=1e-3,
              replay_buffer_max_length=100000, collect_steps_per_iteration=1, num_iterations=5000, log_interval=200,
              eval_interval=1000, loss_fn=common.element_wise_squared_loss):
        game_policy = random_tf_policy.RandomTFPolicy(self.time_step_spec(), self.action_spec(),
                                                        observation_and_action_constraint_splitter=SushiGoRLEnvironment.observation_and_action_constraint_splitter)
        self.qnet = self.create_qnet(fc_layer_params = fc_layer_params)
        self.agent = self.create_agent(agent_type = agent_type, network=self.qnet, learning_rate=learning_rate, loss_fn=loss_fn)

        table_name = 'uniform_table'
        replay_buffer_signature = tensor_spec.from_spec(
            self.agent.collect_data_spec)
        replay_buffer_signature = tensor_spec.add_outer_dim(
            replay_buffer_signature)

        table = reverb.Table(
            table_name,
            max_size=replay_buffer_max_length,
            sampler=reverb.selectors.Uniform(),
            remover=reverb.selectors.Fifo(),
            rate_limiter=reverb.rate_limiters.MinSize(1),
            signature=replay_buffer_signature)

        reverb_server = reverb.Server([table])

        replay_buffer = reverb_replay_buffer.ReverbReplayBuffer(
            self.agent.collect_data_spec,
            table_name=table_name,
            sequence_length=2,
            local_server=reverb_server)

        rb_observer = reverb_utils.ReverbAddTrajectoryObserver(
            replay_buffer.py_client,
            table_name,
            sequence_length=2)
        tf_env = tfpy.TFPyEnvironment(self)
        tf_policy = tf_py_policy.TFPyPolicy(py_tf_eager_policy.PyTFEagerPolicy(
            game_policy, use_tf_function=True))
        py_driver.PyDriver(
            self,
            py_tf_eager_policy.PyTFEagerPolicy(
                game_policy, use_tf_function=True),
            [rb_observer],
            max_steps=initial_collect_steps).run(self.reset())
        dataset = replay_buffer.as_dataset(
            num_parallel_calls=3,
            sample_batch_size=batch_size,
            num_steps=2).prefetch(3)
        iterator = iter(dataset)
        print(iterator)
        self.agent.train = common.function(self.agent.train)
        self.agent.train_step_counter.assign(0)

        time_step = self.reset()

        collect_driver = py_driver.PyDriver(
            self,
            py_tf_eager_policy.PyTFEagerPolicy(
                self.agent.collect_policy, use_tf_function=True),
            [rb_observer],
            max_steps=collect_steps_per_iteration)

        for _ in range(num_iterations):
            time_step, _ = collect_driver.run(time_step)
            experience, unused_info = next(iterator)
            train_loss = self.agent.train(experience).loss
            step = self.agent.train_step_counter.numpy()
            if step % log_interval == 0:
                print('step = {0}: loss = {1}'.format(step, train_loss))
        policy_dir = os.path.join(os.getcwd(), policy_name)
        tf_policy_saver = policy_saver.PolicySaver(self.agent.policy)
        tf_policy_saver.save(policy_dir)


if __name__ == "__main__":
    environment = SushiGoRLEnvironment()
    # utils.validate_py_environment(environment, episodes=5, observation_and_action_constraint_splitter = SushiGoRLEnvironment.observation_and_action_constraint_splitter)
    environment.train('Test2', dqn_agent.DqnAgent, fc_layer_params = (100,50), num_iterations = 400, log_interval = 50)
