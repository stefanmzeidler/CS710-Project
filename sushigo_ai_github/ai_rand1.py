from sushi_state import GameState, SushiCardType
from typing import List
from random import randint

def play_turn(state: GameState) -> List[SushiCardType]:
    size = len(state.hands[0])
    idx = randint(0, size - 1)
    return [state.hands[0][idx]]
