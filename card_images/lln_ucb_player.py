from player import Player
from tf_agents.bandits.agents import lin_ucb_agent
class LinUCBPlayer(Player):
    def __init__(self):
        super().__init__(name = "LinUCB")


    def choose_card(self, game_state):
        ...