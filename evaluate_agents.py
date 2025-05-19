from game_manager import Game
from mcts_player import MCTSPlayer
from random_player import RandomPlayer
import numpy as np
from MCTSNode import MCTSNode
MCTSPLAYER = "MCTS Player"

def run_tournament(num_games=100, evaluation_function = MCTSNode.standard_evaluation, selection_policy = MCTSNode.ucb1, simulations = 40):
    player_names = [MCTSPLAYER, "Rand1", "Rand2"]
    scores = {name: [] for name in player_names}
    wins = {name: 0 for name in player_names}
    ranks = {name: [0, 0, 0] for name in player_names}

    for _ in range(num_games):
        players = [
            MCTSPlayer(MCTSPLAYER, evaluation_function = evaluation_function, selection_policy = selection_policy, simulations = simulations),
            RandomPlayer("Rand1"),
            RandomPlayer("Rand2")
        ]
        game = Game(players)
        game.play()
        game_results = sorted(players, key=lambda p: p.score, reverse=True)
        for idx, player in enumerate(game_results):
            scores[player.name].append(player.score)
            if idx == 0:
                wins[player.name] += 1
            ranks[player.name][idx] += 1

    print("\nTOURNAMENT RESULTS")
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
    run_tournament(num_games=100, selection_policy=MCTSNode.ucb1, simulations = 40)
    # run_tournament(num_games=100,evaluation_function = MCTSNode.posas_evaluation, selection_policy=MCTSNode.ucb1,simulations = 40)
    # run_tournament(num_games =100, selection_policy = MCTSNode.ucbt,simulations = 40)
