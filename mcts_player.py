from player import Player
from collections import defaultdict


class MCTSPlayer(Player):
    def __init__(self, name = "MCTS Player"):
        super().__init__(name)
        self.opponent_hand = None

    def choose_card(self, game_state):
        game_round = game_state['game_round']
        players = game_state['players']
        # TODO rest of logic




        self.opponent_hand = self.hand


    def predict_scores(self, players, hand):
        original_values = defaultdict(list)
        for player in players:
            original_values[player] = [player.score, player.maki_icons, player.pudding_cards, player.chosen_cards, player.hand]
        scores = defaultdict(int)
        for candidate_card in hand:
            ...

        for player in players:
            player.score = original_values[player][0]
            player.maki_icons = original_values[player][1]
            player.pudding_cards = original_values[player][2]
            player.chosen_cards = original_values[player][3]
            player.hand = original_values[player][4]
