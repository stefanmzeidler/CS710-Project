from collections import defaultdict

import numpy as np
import tensorflow as tf
from tf_agents.environments import utils
from tf_agents.environments.py_environment import PyEnvironment
from tf_agents.specs import array_spec
from tf_agents.specs import tensor_spec
from tf_agents.trajectories import time_step as ts
from tf_agents.networks import sequential
from tf_agents.utils import common
from tf_agents.agents.dqn import dqn_agent




from card import Card
from game_manager import Game
from game_utils import score_round
from player import Player
from random_player import RandomPlayer


class SushiGoRLEnvironment(PyEnvironment, Player):
    def __init__(self):
        super().__init__()
        self.name = 'RLPlayer'
        self.categories = [Card.DOUBLE_MAKI, Card.DUMPLING, Card.EGG, Card.PUDDING, Card.SALMON, Card.SASHIMI,
                           Card.SINGLE_MAKI, Card.SQUID, Card.TEMPURA, Card.TRIPLE_MAKI, Card.WASABI]
        players = [self, RandomPlayer("Random1"), RandomPlayer("Random2")]
        self.game = Game(players)
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=len(self.categories) - 1, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(2, len(self.categories)), dtype=np.int32, minimum=0, name='observation')
        self._reward_spec = array_spec.BoundedArraySpec(shape=(), dtype=np.int32, minimum=0, name='reward')
        self._state = np.zeros(len(self.categories), dtype=np.int32)
        self._episode_ended = False
        self.card_to_choose = None

        self.qnet = self.create_qnet()
        self.agent = self.create_agent(network = self.qnet,learning_rate = 1e-3)

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
        self.card_to_choose = Card(self.categories[action])
        if self._episode_ended:
            return self.reset()
        elif self.game.game_round > 3 or self.play_single_turn() is None:
            self._episode_ended = True
        if self._episode_ended:
            reward = self.score
            return ts.termination(np.array([self._state, self.cards_to_vector(self.hand)], dtype=np.int32),
                                  reward=reward)
        else:
            return ts.transition(np.array([self._state, self.cards_to_vector(self.hand)], dtype=np.int32), reward=0,
                                 discount=1.0)

    def play_single_turn(self):
        if self.game.turn > self.game.number_cards:
            self.game.game_round += 1
            if self.game.game_round >= Game.TOTAL_ROUNDS:
                return None
            self.game.turn = 0
            score_round(self.game.players)
            for player in self.game.players:
                player.card_history[self.game.game_round] = player.chosen_cards
        if self.game.turn == 0:
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
        self._state = np.zeros(len(self.categories), dtype=np.int32)
        players = [self, RandomPlayer("Random1"), RandomPlayer("Random1")]
        self.game = Game(players)
        return ts.restart(np.array([self._state, self.cards_to_vector(self.hand)], dtype=np.int32))

    def cards_to_vector(self, card_list):
        card_names = [c.name for c in card_list]
        vector = np.zeros(len(self.categories), dtype=np.int32)
        for name in card_names:
            vector[self.categories.index(name)] += 1
        return vector

    def choose_card(self, game_state):
        return self.card_to_choose


    def create_qnet(self):
        """
        Adapted from https://github.com/tensorflow/agents/blob/master/docs/tutorials/1_dqn_tutorial.ipynb
        :return:
        """
        fc_layer_params = (100, 50)
        action_tensor_spec = tensor_spec.from_spec(self.action_spec())
        num_actions = action_tensor_spec.maximum - action_tensor_spec.minimum + 1

        def dense_layer(num_units):
            return tf.keras.layers.Dense(
                num_units,
                activation=tf.keras.activations.relu,
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

    def create_agent(self,network, learning_rate):
        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        train_step_counter = tf.Variable(0)
        agent = dqn_agent.DqnAgent(
            self.time_step_spec(),
            self.action_spec(),
            q_network=network,
            optimizer=optimizer,
            td_errors_loss_fn=common.element_wise_squared_loss,
            train_step_counter=train_step_counter)
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

environment = SushiGoRLEnvironment()
utils.validate_py_environment(environment, episodes=5)
