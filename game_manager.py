from deck import Deck
from game_utils import *
from collections import defaultdict
import pandas as pd
class Game:
    TOTAL_ROUNDS = 3
    def __init__(self, players):
        self.players = players
        self.deck = None
        self.number_cards = 0
        self.game_round = 0
        self.turn = 0

    def get_game_state(self):
        game_state = defaultdict(list)
        game_state["game_round"] = [self.game_round]
        game_state["players"] = self.players
        game_state['turn'] = [self.turn]
        return game_state

    def play(self):
        for self.game_round in range(Game.TOTAL_ROUNDS):
            self.deal_cards()
            for i in range(self.number_cards+1):
                self.turn = i
                for player in self.players:
                    player.play_turn(self.get_game_state())
                self.pass_hands()
            score_round(self.players)
            for player in self.players:
                player.card_history[self.game_round] = player.chosen_cards
        score_pudding_cards(self.players)
        game_data = defaultdict(list)
        for player in self.players:
            game_data['player_name'].append(player.name)
            game_data['score'].append(player.score)
            for game_round, cards in player.card_history.items():
                game_data[f'round_{game_round+1}'].append(cards)
        return game_data

    def play_single_turn(self):
        if self.turn > self.number_cards:
            self.game_round += 1
            self.turn = 0
        if self.game_round >= Game.TOTAL_ROUNDS:
            return None
        if self.turn == 0:
            self.deal_cards()
        for player in self.players:
            player.play_turn(self.get_game_state())
        self.pass_hands()
        self.turn += 1
        return self.get_game_state()

    def deal_cards(self):
        try:
            self.number_cards = {2:10, 3:9, 4:8, 5:7}.get(len(self.players))
        except IndexError:
            print("Incorrect number of players")
            exit(1)
        self.deck = Deck(self.get_pudding_cards())
        for player in self.players:
            player.chosen_cards = []
            for i in range(self.number_cards+1):
                player.hand.append(self.deck.deal())

    def get_pudding_cards(self) -> int:
        pudding_cards = 0
        for player in self.players:
            pudding_cards += player.pudding_cards
        return pudding_cards

    def print_player_hands(self):
        for player in self.players:
            print(player.name, player.hand)

    def pass_hands(self):
        hands = [player.hand for player in self.players]
        for index, player in enumerate(self.players):
            player.hand = hands[(index+1)% len(self.players)]
