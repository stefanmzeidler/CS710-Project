from sushi_state import GameState, SushiCardType
from typing import List, Callable
from random import randint


def get_play_turn(preference: SushiCardType) -> Callable[[GameState], List[SushiCardType]]:
    def play_turn(state: GameState) -> List[SushiCardType]:
        pref_idxs = [i for i, n in enumerate(state.hands[0]) if n == preference]
        size = len(state.hands[0])
        if len(pref_idxs) > 0:
            idx1 = pref_idxs[0]
        else:
            idx1 = randint(0, size - 1)
        idxs = [state.hands[0][idx1]]
        if len(state.hands[0]) > 1 and SushiCardType.CHOPSTICKS in state.played_cards[0]:
            if len(pref_idxs) > 1:
                idx2 = pref_idxs[1]
            else:
                idx2 = randint(0, size - 2)
                if idx2 >= idx1:
                    idx2 += 1
            idxs += [state.hands[0][idx2]]
        return idxs
    return play_turn

