from deck import Deck
from game_utils import *
from collections import defaultdict
class Game:
    def __init__(self, players):
        self.players = players
        self.deck = None
        self.number_cards = 0
        self.game_round = 0

    def get_game_state(self):
        game_state = defaultdict(list)
        game_state["game_round"] = [self.game_round]
        game_state["players"] = self.players

        ...
    def play(self):
        for self.game_round in range(3):
            print(self.game_round)
            # if game_round > 0:
            #     assert(len(self.deck.cards) < 104)
            self.deal_cards()
            for i in range(self.number_cards+1):
                for player in self.players:
                    player.play_turn(self.get_game_state())
                self.pass_hands()
            score_round(self.players)
            for player in self.players:
                player.card_history[self.game_round] = player.chosen_cards
        score_pudding_cards(self.players)
        for player in self.players:
            print(player.name, " : ", player.score)
            for game_round, cards in player.card_history.items():
                print(f"{game_round} : {chosen_cards_to_strings(cards)}")

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
