import os

import numpy as np
import tensorflow as tf
from tf_agents.trajectories import time_step as ts
from tf_agents.utils import nest_utils

from card import Card
from player import Player
from reinforcement_environment import SushiGoRLEnvironment as sge


class RLPlayer(Player):
    def __init__(self, policy_name):
        super().__init__(name="RLPlayer")
        policy_dir = os.path.join(os.getcwd(), policy_name)
        self.policy = tf.saved_model.load(policy_dir)

    def choose_card(self, game_state) -> Card:
        game_turn = game_state['turn'][0]
        game_round = game_state['game_round'][0]
        number_cards = {2: 10, 3: 9, 4: 8, 5: 7}.get(len(game_state['game_players']))
        if game_turn == 0 and game_round == 1:
            step_type = 1
        elif game_turn == 3 and game_turn == number_cards:
            step_type = 2
        else:
            step_type = 3
        action_step = self.policy.action(self.create_timestep(step_type))
        card_name = sge.CATEGORIES[action_step.action[0]]
        return next(hand_card for hand_card in self.hand if hand_card.name == card_name)

    def create_timestep(self, step_type):
        state = sge.cards_to_vector(self.chosen_cards)
        mask = sge.hand_to_action_mask(self.hand)
        observation = {'observation': state, 'mask': mask}
        time_step = ts.TimeStep(
            step_type=np.int32(step_type),
            observation=observation,
            reward=np.float32(0.0),
            discount=np.float32(1.0)
        )

        return nest_utils.batch_nested_array(time_step)
