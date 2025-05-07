import card
from card import Card
from random import shuffle

class Deck:
    def __init__(self, pudding = 0):
        self.cards = []
        for i in range(14):
            self.cards.append(Card(card.TEMPURA))
            self.cards.append(Card(card.SASHIMI))
            self.cards.append(Card(card.DUMPLING))
        for i in range(12):
            self.cards.append(Card(card.DOUBLE_MAKI))
        for i in range(10):
            self.cards.append(Card(card.SALMON))
        for i in range(8):
            self.cards.append(Card(card.TRIPLE_MAKI))
        for i in range(6):
            self.cards.append(Card(card.SINGLE_MAKI))
            self.cards.append(Card(card.WASABI))
        for i in range(5):
            self.cards.append(Card(card.SQUID))
            self.cards.append(Card(card.EGG))
        for i in range(10 - pudding):
            self.cards.append(Card(card.PUDDING))
        # for i in range(4):
        #     self.cards.append(Card(card.CHOPSTICKS))
        shuffle(self.cards)

    def deal(self) -> Card:
        return self.cards.pop()

    def print_deck(self):
        for deck_card in self.cards:
            print(deck_card.name)

if __name__ == '__main__':
    deck = Deck()
    deck.print_deck()