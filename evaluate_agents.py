from game_manager import Game
from mcts_player import MCTSPlayer
from random_player import RandomPlayer
import numpy as np
MCTSPLAYER = "MCTS Player"

def run_tournament(num_games=100):
    player_names = [MCTSPLAYER, "Rand1", "Rand2"]
    scores = {name: [] for name in player_names}
    wins = {name: 0 for name in player_names}
    ranks = {name: [0, 0, 0] for name in player_names}  # 1st, 2nd, 3rd

    for _ in range(num_games):
        # Instantiate fresh players each game
        players = [
            MCTSPlayer(MCTSPLAYER, 10),
            RandomPlayer("Rand1"),
            RandomPlayer("Rand2")
        ]
        game = Game(players)
        game.play()

        # Collect scores
        game_results = sorted(players, key=lambda p: p.score, reverse=True)
        for idx, player in enumerate(game_results):
            scores[player.name].append(player.score)
            if idx == 0:
                wins[player.name] += 1
            ranks[player.name][idx] += 1

    # Print summary
    print("\n📊 TOURNAMENT RESULTS")
    for name in player_names:
        avg = np.mean(scores[name])
        std = np.std(scores[name])
        winrate = (wins[name] / num_games) * 100
        print(f"\n{name}")
        print(f"  Avg Score: {avg:.2f}")
        print(f"  Std Dev:   {std:.2f}")
        print(f"  Wins:      {wins[name]} ({winrate:.1f}%)")
        print(f"  1st/2nd/3rd: {ranks[name]}")

if __name__ == "__main__":
    run_tournament(100)
