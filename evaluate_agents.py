from game_manager import Game
from mcts_player import MCTSPlayer
from random_player import RandomPlayer
import numpy as np
from MCTSNode import MCTSNode
from rl_player import RLPlayer

def run_tournament(player_types, policy_name = None, num_games=100,evaluation_function = MCTSNode.standard_evaluation, selection_policy = MCTSNode.ucb1, simulations = 40):
    if len(player_types) != 3:
        raise ValueError("Tournament must have 3 players")

    def player_factory(class_types):
        for index, class_type in enumerate(class_types):
            if class_type is RandomPlayer:
                yield RandomPlayer(name = f"Random{index}")
            elif class_type is MCTSPlayer:
                if evaluation_function is None or selection_policy is None or simulations <= 0:
                    raise ValueError('Invalid MCTS parameters')
                yield MCTSPlayer(evaluation_function = evaluation_function, selection_policy = selection_policy, simulations = simulations)
            elif class_type is RLPlayer:
                if policy_name is None:
                    raise ValueError('Invalid policy name')
                yield RLPlayer(policy_name = policy_name)
            else:
                raise ValueError('Invalid player type')

    temp_players = list(player_factory(player_types))
    player_names = [game_player.name for game_player in temp_players]
    scores = {name: [] for name in player_names}
    wins = {name: 0 for name in player_names}
    ranks = {name: [0, 0, 0] for name in player_names}



    for _ in range(num_games):
        # players = [
        #     MCTSPlayer(MCTSPLAYER, evaluation_function = evaluation_function, selection_policy = selection_policy, simulations = simulations),
        #     RandomPlayer("Rand1"),
        #     RandomPlayer("Rand2")
        # ]
        players = list(player_factory(player_types))
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
    game_player_types = [MCTSPlayer, RandomPlayer, RandomPlayer]
    run_tournament(player_types = game_player_types, policy_name="Tripe100Layers3000Iterations", num_games=100, selection_policy=MCTSNode.ucb1, simulations = 10)
