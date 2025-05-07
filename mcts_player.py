import player
from player import Player
import copy
from MCTSNode import MCTSNode

class MCTSPlayer(Player):
    def __init__(self, name = player.MCTSPLAYER, simulations=40):
        super().__init__(name)
        self.opponent_hand = None
        self.simulations = simulations

    def choose_card(self, game_state):
        root = MCTSNode(copy.deepcopy(game_state['players']))

        for _ in range(self.simulations):  # Number of simulations
            node = root
            while node.is_fully_expanded() and node.children:
                node = node.best_child()
            if not node.is_fully_expanded():
                node = node.expand()
            reward = node.get_reward()
            node.backpropagate(reward)

        best_node = root.best_child(c_param=0)
        return best_node.action

    def simulate_full_game(self, players, initial_card):
        from game_utils import score_round, score_pudding_cards
        import random
        import copy
        players = [copy.deepcopy(p) for p in players]
        sim_self = next(p for p in players if p.name == self.name)
        sim_self.hand.remove(initial_card)
        sim_self.add_to_set(initial_card)
        for p in players:
            if p.name != self.name:
                rand_card = random.choice(p.hand)
                p.hand.remove(rand_card)
                p.add_to_set(rand_card)
        for _ in range(3):
            while len(players[0].hand) > 0:
                for p in players:
                    if len(p.hand) == 0:
                        continue
                    chosen = random.choice(p.hand)
                    p.hand.remove(chosen)
                    p.add_to_set(chosen)
            score_round(players)
            for p in players:
                p.hand = []
                p.chosen_cards = []
            from deck import Deck
            deck = Deck(pudding=sum(p.pudding_cards for p in players))
            hand_size = {2: 10, 3: 9, 4: 8, 5: 7}.get(len(players), 9)
            for p in players:
                for _ in range(hand_size):
                    p.hand.append(deck.deal())
        score_pudding_cards(players)
        return next(p for p in players if p.name == self.name).score