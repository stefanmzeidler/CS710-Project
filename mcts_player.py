import player
from player import Player
from collections import defaultdict
import copy
from MCTSNode import MCTSNode
import random
import game_utils
class MCTSPlayer(Player):
    def __init__(self, name = player.MCTSPlayer):
        super().__init__(name)
        self.opponent_hand = None

    # def clone(self) -> Player:
    #     return deepcopy(self)

        # copy = MCTSPlayer()
        # copy.hand = [Card(hand_card.name) for hand_card in self.hand]
        # copy.chosen_cards = [Card(chosen_card.name)for chosen_card in self.chosen_cards]
        # copy.maki_icons = self.maki_icons
        # copy.pudding_cards = self.pudding_cards
        # return copy

    # def choose_card(self, game_state):
    #     game_round = game_state['game_round']
    #     players = game_state['players']
    #
    #
    #     # TODO rest of logic
    #     self.opponent_hand = self.hand

    def choose_card(self, game_state):
        root = MCTSNode(copy.deepcopy(game_state['players']))

        for _ in range(40):  # Number of simulations
            node = root

            # 1. Selection
            while node.is_fully_expanded() and node.children:
                node = node.best_child()

            # 2. Expansion
            if not node.is_fully_expanded():
                node = node.expand()

            # 3. Simulation returns score directly now
            reward = node.get_reward()
            # reward = node.state  # simulate_action() returns the score now

            # 4. Backpropagation
            node.backpropagate(reward)

        best_node = root.best_child(c_param=0)
        return best_node.action

    # def simulate_playout(self, players, chosen_card):
    #     sim_players = [p.clone() for p in players]
    #     sim_self = next(p for p in players if p.name == self.name)
    #
    #     for p in sim_players:
    #         if p.name != self.name:
    #             chosen = random.choice(p.hand)
    #             p.hand.remove(chosen)
    #             p.add_to_set(chosen)
    #     game_utils.score_round(sim_players)
    #     return next(p for p in sim_players if p.name == self.name)

    def simulate_full_game(self, players, initial_card):
        from game_utils import score_round, score_pudding_cards
        import random
        import copy

        # Deep copy of all players
        players = [copy.deepcopy(p) for p in players]
        sim_self = next(p for p in players if p.name == self.name)

        # Apply the initial action
        sim_self.hand.remove(initial_card)
        sim_self.add_to_set(initial_card)
        for p in players:
            if p.name != self.name:
                rand_card = random.choice(p.hand)
                p.hand.remove(rand_card)
                p.add_to_set(rand_card)

        # Simulate 3 rounds
        for _ in range(3):
            # Complete all remaining turns of the round
            while len(players[0].hand) > 0:
                for p in players:
                    if len(p.hand) == 0:
                        continue
                    chosen = random.choice(p.hand)
                    p.hand.remove(chosen)
                    p.add_to_set(chosen)

            # Score the round
            score_round(players)

            # Clear hands for next round
            for p in players:
                p.hand = []
                p.chosen_cards = []

            # Re-deal cards for new round
            from deck import Deck
            deck = Deck(pudding=sum(p.pudding_cards for p in players))
            hand_size = {2: 10, 3: 9, 4: 8, 5: 7}.get(len(players), 9)
            for p in players:
                for _ in range(hand_size):
                    p.hand.append(deck.deal())

        # Score pudding at the end
        score_pudding_cards(players)

        return next(p for p in players if p.name == self.name).score

    # def predict_scores(self, players, hand):
    #     original_values = defaultdict(list)
    #     for player in players:
    #         original_values[player] = [player.score, player.maki_icons, player.pudding_cards, player.chosen_cards, player.hand]
    #     scores = defaultdict(int)
    #     for candidate_card in hand:
    #         ...
    #
    #     for player in players:
    #         player.score = original_values[player][0]
    #         player.maki_icons = original_values[player][1]
    #         player.pudding_cards = original_values[player][2]
    #         player.chosen_cards = original_values[player][3]
    #         player.hand = original_values[player][4]
