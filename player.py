from abc import ABC, abstractmethod
from collections import defaultdict
import card
import copy
from card import Card
MCTSPLAYER = "MCTS Player"
class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.card_history = defaultdict(list)
        self.chosen_cards = []
        self.maki_icons = 0
        self.pudding_cards = 0
        self.score = 0
        self.last_played = None

    def __str__(self):
        return str(self.name)
    def __repr__(self):
        return str(self.name)

    def add_to_set(self, new_card):
        match new_card.name:
            case card.SQUID | card.SALMON | card.EGG:
                duplicate = False
                for chosen_card in self.chosen_cards:
                    if chosen_card.name == card.WASABI and chosen_card.next is None:
                        chosen_card.next = new_card
                        duplicate = True
                        break
                if not duplicate:
                    self.chosen_cards.append(new_card)
            case _:
                self.chosen_cards.append(new_card)

    def play_turn(self, game_state):
        chosen_card = self.choose_card(game_state)
        self.add_to_set(chosen_card)
        self.remove_card(chosen_card)
        self.last_played = chosen_card
        # self.hand.remove(chosen_card)

    def clone(self):
        return copy.deepcopy(self)

    def remove_card(self, my_card):
        for hand_card in self.hand:
            if my_card.name == hand_card.name:
                self.hand.remove(hand_card)
                break

    @abstractmethod
    def choose_card(self, game_state) -> Card:
        pass
# def invariant_check(self):
#     for card in self.chosen_cards:




