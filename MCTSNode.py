import math
import random
import copy

class MCTSNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.total_reward = 0
        self.untried_actions = self.get_legal_actions()
        self.action = action

    def get_reward(self):
        my_player = self.get_self_player()
        return my_player.score

    def get_legal_actions(self):
        my_player = self.get_self_player()
        return my_player.hand[:]

    def get_self_player(self):
        return next(p for p in self.state if p.name == "MCTS Player")

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            (child.total_reward / child.visits) + c_param * math.sqrt(math.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.simulate_action(self.state, action)
        child_node = MCTSNode(next_state, parent=self, action=action)
        self.children.append(child_node)
        return child_node

    @staticmethod
    def simulate_action(self, players, my_card):
        from game_utils import score_round
        simulated_players = [copy.deepcopy(p) for p in players]
        sim_self = next(p for p in simulated_players if p.name == "MCTS Player")
        sim_self.remove_card(my_card)
        sim_self.add_to_set(my_card)

        for p in simulated_players:
            if p.name != "MCTS Player":
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
        if self.parent:
            self.parent.back_propagate(reward)
