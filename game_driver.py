from game_manager import Game
from random_player import RandomPlayer

def main():
    players = [RandomPlayer("Random1"), RandomPlayer("Random2"), RandomPlayer("Random3")]
    game = Game(players)
    game.play()

main()
# fruits = ["apple", "banana", "orange"]
# for index, fruit in enumerate(fruits):
#     print(fruits[(index + 1) % len(fruits)])