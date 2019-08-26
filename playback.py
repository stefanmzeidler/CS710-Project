from sushi_state import GameStateSet, GameState
from typing import List

class GameRecorder:
    def __init__(self):
        self.turns = GameStateSet.parse_obj({'states':[]})

    def save_state(self, state: GameState):
        self.turns.states.append(state.copy(deep=True))

    def write_file(self, fd):
        fd.write(self.turns.json())
