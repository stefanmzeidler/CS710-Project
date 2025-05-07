import math
import random
import copy
import player

class MCTSNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.total_reward = 0
        self.untried_actions = self.get_legal_actions()
        self.action = action

    def get_legal_actions(self):
        my_player = self.get_self_player()
        return my_player.hand[:]

    def get_self_player(self):
        return next(p for p in self.state if p.name == player.MCTSPlayer)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c=1.4):
        choices_weights = [
            (child.total_reward / child.visits) + c * math.sqrt(math.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.simulate_action(self.state, action)
        child_node = MCTSNode(next_state, parent=self, action=action)
        self.children.append(child_node)
        return child_node

    # @staticmethod
    # def simulate_action(players, my_card):
    #     from game_utils import score_round
    #
    #     simulated_players = [copy.deepcopy(p) for p in players]
    #     sim_self = next(p for p in simulated_players if p.name == player.MCTSPlayer)
    #     sim_self.hand.remove(my_card)
    #     sim_self.add_to_set(my_card)
    #
    #     for p in simulated_players:
    #         if p.name != player.MCTSPlayer:
    #             choice = random.choice(p.hand)
    #             p.hand.remove(choice)
    #             p.add_to_set(choice)
    #
    #     score_round(simulated_players)
    #     return simulated_players


    @staticmethod
    def simulate_action(players, my_card):
        from mcts_player import MCTSPlayer
        sim_agent = MCTSPlayer(name="MCTS Player")
        return_score = sim_agent.simulate_full_game(players, my_card)
        return return_score  # Just returning score now

    def back_propagate(self, reward):
        self.visits += 1
        self.total_reward += reward
        if self.parent:
            self.parent.back_propagate(reward)
