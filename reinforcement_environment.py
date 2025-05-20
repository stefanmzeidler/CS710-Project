import tensorflow as tf
from tf_agents.specs import array_spec
import numpy as np
from tf_agents.trajectories import time_step as ts
from tf_agents.typing import types
from collections import defaultdict
from game_utils import score_round
import random
from game_manager import Game
from player import Player
from random_player import RandomPlayer
from tf_agents.environments.py_environment import PyEnvironment
from card import Card
from tf_agents.environments import utils



class SushiGoRLEnvironment(PyEnvironment, Player):
    def __init__(self):
        super().__init__()
        self.name = 'RLPlayer'
        self.categories = [Card.DOUBLE_MAKI, Card.DUMPLING, Card.EGG, Card.PUDDING, Card.SALMON, Card.SASHIMI,
                      Card.SINGLE_MAKI, Card.SQUID, Card.TEMPURA, Card.TRIPLE_MAKI, Card.WASABI]
        players = [self, RandomPlayer("Random1"), RandomPlayer("Random2")]
        self.game = Game(players)
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=10, name='action')
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(2, len(self.categories)), dtype=np.int32, minimum=0, name='observation')
        self._reward_spec = array_spec.BoundedArraySpec(shape =(), dtype=np.int32, minimum=0, name='reward')
        self._state = np.zeros(len(self.categories), dtype=np.int32)
        self._episode_ended = False

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _step(self, action: types.NestedArray) -> ts.TimeStep:
        if self._episode_ended:
            return self.reset()
        elif self.game.game_round > 3 or self.play_single_turn() is None:
            self._episode_ended = True
        if self._episode_ended:
            reward = self.score
            return ts.termination(np.array([self._state, self.cards_to_vector(self.hand)], dtype=np.int32), reward = reward)
        else:
            return ts.transition(np.array([self._state, self.cards_to_vector(self.hand)], dtype=np.int32), reward = 0, discount = 1.0)

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
            vector[self.categories.index(name)] +=1
        return vector

    def choose_card(self,game_state):
        return random.choice(self.hand)

environment = SushiGoRLEnvironment()
utils.validate_py_environment(environment, episodes=5)