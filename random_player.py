import player
import random

class RandomPlayer(player.Player):
    def __init__(self, name = "Random Player"):
        super().__init__(name)

    def choose_card(self, game_state):
        return random.choice(self.hand)