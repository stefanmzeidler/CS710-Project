from sushi_state import GameState, SushiCardType
from typing import List
from random import randint

def play_turn(state: GameState) -> List[SushiCardType]:
    size = len(state.hands[0])
    idx1 = randint(0, size - 1)
    idxs = [state.hands[0][idx1]]
    if len(state.hands[0]) > 1 and SushiCardType.CHOPSTICKS in state.played_cards[0]:
        idx2 = randint(0, size - 2)
        if idx2 >= idx1:
            idx2 += 1
        idxs += [state.hands[0][idx2]]
    return idxs
