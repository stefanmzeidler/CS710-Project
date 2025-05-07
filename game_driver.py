import pandas as pd

from game_manager import Game
from random_player import RandomPlayer
from mcts_player import MCTSPlayer
from human_player import HumanPlayer
def main():
    players = [
        HumanPlayer("You"),
        MCTSPlayer(),
        RandomPlayer("RandomBot"),
    ]
    game = Game(players)
    game.play()
    # players = [MCTSPlayer(), RandomPlayer("Random2"), RandomPlayer("Random3")]
    # game = Game(players)
    # game_data = game.play()

# def multiple_runs(n = 10):
#     multiple_run_data = pd.DataFrame
#     for i in range(n):
#         players = [MCTSPlayer(), RandomPlayer("Random2"), RandomPlayer("Random3")]
#         game = Game(players)
#         game_data = game.play()

main()
# fruits = ["apple", "banana", "orange"]
# for index, fruit in enumerate(fruits):
#     print(fruits[(index + 1) % len(fruits)])