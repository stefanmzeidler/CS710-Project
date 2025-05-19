from game_manager import Game
from game_ui import GameUI
from human_player_gui import HumanPlayerGUI
from mcts_player import MCTSPlayer
from random_player import RandomPlayer
from game_utils import score_round
from game_utils import score_pudding_cards
from MCTSNode import MCTSNode
def main():
    mcts_player = MCTSPlayer()
    # mcts_player = MCTSPlayer()
    ui = GameUI()
    human = HumanPlayerGUI("You", ui)
    opponents = [mcts_player, RandomPlayer("RandBot")]
    players = [human] + opponents
    game = Game(players)
    orig_play_turns = game.play

    def custom_play():
        for game.game_round in range(3):
            game.deal_cards()
            for i in range(game.number_cards + 1):
                for player in game.players:
                    player.play_turn(game.get_game_state())
                ui.update_scores(game.players)
                ui.update_table_state(game.players, human.name)
                ui.root.update()
                game.pass_hands()
            score_round(game.players)
        score_pudding_cards(game.players)
        ui.update_scores(game.players)
        ui.prompt_label.config(text="Game Over!")
        ui.root.mainloop()
    game.play = custom_play
    game.play()


main()
