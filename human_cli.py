from sushi_state import GameState, SushiCardType
from typing import List
from random import randint

def play_turn(state: GameState) -> List[SushiCardType]:
    print(f'\tSCORE: {state.scores[0]}')
    print(f'\tPUDDINGS: {state.puddings[0]}') 
    print('\tPLAYED')
    for card in state.played_cards[0]:
        print(f'\t\t{card.value}')
    print('\tHAND')
    for i, card in enumerate(state.hands[0]):
        print(f'\t\t{i}: {card.value}') 
    idx1 = None
    while idx1 is None:
        sel = input('Select valid card: ')
        try:
            idx1 = int(sel)
            if idx1 < 0 or idx1 >= len(state.hands[0]):
                idx1 = None
        except ValueError:
            pass
    idxs = [state.hands[0][idx1]]
    if len(state.hands[0]) > 1 and SushiCardType.CHOPSTICKS in state.played_cards[0]:
        sel = input('Choose a second card? (y/n): ')
        if sel == 'y':
            while idx2 is None:
                sel = input('Select valid card: ')
                try:
                    idx2 = int(sel)
                    if idx1 == idx2 or idx2 < 0 or idx2 >= len(state.hands[0]):
                        idx2 = None
                    idxs += [state.hands[0][idx2]]
                except ValueError:
                    pass
    return idxs
