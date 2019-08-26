from sushi_state import GameState
from typing import List

class GameRecorder:
    def __init__(self):
        self.states: List[GameState] = []

    def save_state(self, state: GameState):
        self.states.append(state.copy(deep=True))

    def write_file(self, fd):
        fd.write('[')
        fd.write(','.join(state.json() for state in self.states))
        fd.write(']')
