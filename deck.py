import card
from card import Card
from random import shuffle

class Deck:
    def __init__(self, pudding = 0):
        self.cards = []
        for i in range(14):
            self.cards.append(Card(Card.TEMPURA))
            self.cards.append(Card(Card.SASHIMI))
            self.cards.append(Card(Card.DUMPLING))
        for i in range(12):
            self.cards.append(Card(Card.DOUBLE_MAKI))
        for i in range(10):
            self.cards.append(Card(Card.SALMON))
        for i in range(8):
            self.cards.append(Card(Card.TRIPLE_MAKI))
        for i in range(6):
            self.cards.append(Card(Card.SINGLE_MAKI))
            self.cards.append(Card(Card.WASABI))
        for i in range(5):
            self.cards.append(Card(Card.SQUID))
            self.cards.append(Card(Card.EGG))
        for i in range(10 - pudding):
            self.cards.append(Card(Card.PUDDING))
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