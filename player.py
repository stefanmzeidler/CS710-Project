from abc import ABC, abstractmethod
from collections import defaultdict
import card
from card import Card

class Player(ABC):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.card_history = defaultdict(list)
        self.chosen_cards = []
        self.maki_icons = 0
        self.pudding_cards = 0
        self.score = 0

    def __str__(self):
        return str(self.name)
    def __repr__(self):
        return str(self.name)

    def add_to_set(self, new_card):
        match new_card.name:
            # case card.SINGLE_MAKI:
            #     self.maki_icons += 1
            #     self.chosen_cards.append(new_card)
            # case card.DOUBLE_MAKI:
            #     self.maki_icons += 2
            #     self.chosen_cards.append(new_card)
            # case card.TRIPLE_MAKI:
            #     self.maki_icons += 3
            #     self.chosen_cards.append(new_card)
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
            # case card.PUDDING:
            #     self.pudding_cards += 1
            #     self.chosen_cards.append(new_card)
            # case card.TEMPURA | card.SASHIMI | card.DUMPLING | card.WASABI | card.CHOPSTICKS:
            #     self.chosen_cards.append(new_card)

    @abstractmethod
    def choose_card(self, game_state) -> Card:
        pass

    def play_turn(self, game_state):
        chosen_card = self.choose_card(game_state)
        self.add_to_set(chosen_card)
        self.hand.remove(chosen_card)

# def invariant_check(self):
#     for card in self.chosen_cards:




