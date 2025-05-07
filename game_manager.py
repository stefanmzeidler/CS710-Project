from deck import Deck
from game_utils import *
from collections import defaultdict
import pandas as pd
class Game:
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
        for self.game_round in range(3):
            print(f"Starting round: {self.game_round}")
            # if game_round > 0:
            #     assert(len(self.deck.cards) < 104)
            self.deal_cards()
            for i in range(self.number_cards+1):
                self.turn = i
                for player in self.players:
                    player.play_turn(self.get_game_state())
                for player in self.players:
                    print(f"{player.name} chose {player.last_played}. {player.name}'s chosen cards are: {player.chosen_cards}")
                self.pass_hands()
            score_round(self.players)
            for player in self.players:
                player.card_history[self.game_round] = player.chosen_cards
        score_pudding_cards(self.players)
        game_data = defaultdict(list)
        # game_data['players'] = self.players
        for player in self.players:
            game_data['player_name'].append(player.name)
            game_data['score'].append(player.score)
            print(player.name, " : ", player.score)
            for game_round, cards in player.card_history.items():
                game_data[f'round_{game_round+1}'].append(cards)
                print(f"{game_round} : {chosen_cards_to_strings(cards)}")
        return game_data

    def deal_cards(self):
        try:
            self.number_cards = {2:10, 3:9, 4:8, 5:7}.get(len(self.players))
        except IndexError:
            print("Incorrect number of players")
            exit(1)
        # match len(self.players):
        #     case 2:
        #         self.number_cards = 10
        #     case 3:
        #         self.number_cards = 9
        #     case 4:
        #         self.number_cards = 8
        #     case 5:
        #         self.number_cards = 7
        #     case _:
        #         raise ValueError("Incorrect number of players")
        self.deck = Deck(self.get_pudding_cards())
        for player in self.players:
            player.chosen_cards = []
            for i in range(self.number_cards+1):
                player.hand.append(self.deck.deal())

    # def score_hand(self, hand):
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
