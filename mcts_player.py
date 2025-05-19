import copy

import player
from MCTSNode import MCTSNode
from player import Player


class MCTSPlayer(Player):
    def __init__(self, name=player.MCTSPLAYER, evaluation_function=MCTSNode.standard_evaluation,
                 selection_policy=MCTSNode.ucb1, c_param=1.4, simulations=40):
        super().__init__(name)
        self.c_param = c_param
        self.opponent_hand = None
        self.simulations = simulations
        self.evaluation_function = evaluation_function
        self.selection_policy = selection_policy

    def choose_card(self, game_state):
        root = MCTSNode(copy.deepcopy(game_state['players']), player_name=self.name,
                        evaluation_function=self.evaluation_function, selection_policy=self.selection_policy)
        for _ in range(self.simulations):
            node = root
            while node.is_fully_expanded() and node.children:
                node = node.best_child(c_param=self.c_param)
            if not node.is_fully_expanded():
                node = node.expand()
            reward = node.get_reward()
            node.back_propagate(reward)

        best_node = root.best_child(c_param=0)
        return best_node.action

