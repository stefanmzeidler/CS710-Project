from sushi_state import GameState, SushiCardType, get_shuffled_cards
from typing import List
from random import randint
from functools import reduce
import operator as op

def play_turn(state: GameState) -> List[SushiCardType]:
    # If cards are unknown, assign the randomly
    combined_hands = reduce(op.concat, state.hands)
    if SushiCardType.HIDDEN in combined_hands:
        hands: List[List[SushiCardType]] = []
        cards_left = get_shuffled_cards()
        for card in state.discard_pile:
            cards_left.remove(card)
        for card in combined_hands:
            if card != SushiCardType.HIDDEN:
                cards_left.remove(card)
        for card in reduce(op.concat, state.played_cards):
            cards_left.remove(card)
        for _ in range(reduce(op.add, state.puddings)):
            cards_left.remove(SushiCardType.PUDDING)
        for hand in state.hands:
            if SushiCardType.HIDDEN in hand:
                hand = list(hand)
                for i, card in enumerate(hand):
                    if card == SushiCardType.HIDDEN:
                        hand[i] = cards_left.pop()
            hands.append(hand)
    else:
        hands = state.hands
    
    

    return [state.hands[0][idx]]
