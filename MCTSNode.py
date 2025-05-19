import copy
import math
import random

import numpy as np
from scipy.stats import t

from game_utils import score_round


class MCTSNode:
    def __init__(self, state, player_name, evaluation_function, selection_policy, parent=None, action=None):
        self.state = state
        self.player_name = player_name
        self.evaluation_function = evaluation_function
        self.selection_policy = selection_policy
        self.parent = parent
        self.children = []
        self.visits = 0
        self.total_reward = 0
        self.untried_actions = self.get_legal_actions()
        self.action = action
        self.squared_reward_sum = 0.0

    def get_reward(self):
        my_player = self.get_self_player()
        return my_player.score

    def get_legal_actions(self):
        my_player = self.get_self_player()
        return my_player.hand[:]

    def get_self_player(self):
        return next(p for p in self.state if p.name == self.player_name)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def mean_reward(self):
        if self.visits == 0:
            return 0.0
        return self.total_reward / self.visits

    def sample_standard_deviation(self):
        if self.visits < 2:
            return float("inf")
        variance = (self.squared_reward_sum - (self.squared_reward_sum / self.visits)) / (self.visits - 1)
        return math.sqrt(variance)

    @staticmethod
    def standard_evaluation(weights):
        return weights.index(max(weights))

    @staticmethod
    def posas_evaluation(weights):
        def ramp_function(value):
            return max(0, value)

        i_h = 0.5 * np.std(weights)

        def score(value):
            return -ramp_function(abs(value) - i_h)

        posas_weights = [score(weight) for weight in weights]
        return posas_weights.index(max(posas_weights))

    @staticmethod
    def ucb1(**kwargs):
        parent = kwargs.get('parent')
        child = kwargs.get('child')
        c_param = kwargs.get('c_param')
        return (child.total_reward / child.visits) + c_param * math.sqrt(math.log(parent.visits) / child.visits)

    @staticmethod
    def ucbt(**kwargs):
        child = kwargs.get('child')
        mean = child.mean_reward()
        t_score = t.ppf(.99, child.visits - 1)
        sample_standard_deviation = child.sample_standard_deviation()
        return mean + ((t_score * sample_standard_deviation) / math.sqrt(child.visits))

    def best_child(self, c_param=1.4):
        choices_weights = [self.selection_policy(parent=self, child=child, c_param=c_param) for child in self.children]
        return self.children[self.evaluation_function(choices_weights)]

    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.simulate_action(self.state, action)
        child_node = MCTSNode(next_state, player_name=self.player_name, evaluation_function=self.evaluation_function,
                              selection_policy=self.selection_policy, parent=self, action=action)
        self.children.append(child_node)
        return child_node

    def simulate_action(self, players, my_card):
        simulated_players = [copy.deepcopy(p) for p in players]
        sim_self = next(p for p in simulated_players if p.name == self.player_name)
        sim_self.remove_card(my_card)
        sim_self.add_to_set(my_card)
        for p in simulated_players:
            if p.name != self.player_name:
                if len(p.hand) == 0:
                    break
                choice = random.choice(p.hand)
                p.remove_card(choice)
                p.add_to_set(choice)
        score_round(simulated_players)
        return simulated_players

    def back_propagate(self, reward):
        self.visits += 1
        self.total_reward += reward
        self.squared_reward_sum += reward * reward
        if self.parent:
            self.parent.back_propagate(reward)
