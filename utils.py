
from sushi_state import GameState ,SushiCardType, count_card_types, TOTAL_CARD_COUNTS, TOTAL_CARDS
from typing import List, Dict
from functools import reduce
import operator as op
from math import factorial


def ncr(n, r):
    assert(n >= r)
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom
 
# Probability that for [count] items out of [total] total, if [num_picks] are chosen
# without replacement, none of the [count] items are picked
    #[a, b, c, d, e]
    # ? ?
    # ab ac ad ae bc bd be cd ce de
    # 4 / 5 * 3 / 4 = 12 / 20 = 3 / 5 

    #[a, a, c, d, e]
    # ? ?
    # aa ac ad ae ac ad ae cd ce de
    # 3 / 5 * 2 / 4 = 3 / 10 

    #[a, a, c, d, e]
    # ? ? ?
    # aac aad aae acd ace ade  acd ace ade  cde
    # 3 / 5 * 2 / 4 * 1 / 3 = 1 / 10
def prob_no_picks(total: int, count: int, num_picks: int) -> float:
    assert(total >= count)
    assert(total >= num_picks)
    if num_picks > count:
        tmp = count
        count = num_picks
        num_picks = tmp
    r = total - count
    if num_picks > r:
        return 1.0
    numer = reduce(op.mul, range(r, r - num_picks, -1), 1)
    denom = reduce(op.mul, range(total , total - num_picks, -1), 1)
    return numer / denom

# Based on a board state, returns the probility that at least one of the
# unknown cards is that type, for each card type
def card_type_probabilities(state: GameState) -> Dict[SushiCardType, float]:
    known_cards = state.discard_pile
    known_cards += reduce(op.concat, state.hands)
    known_cards += reduce(op.concat, state.played_cards)
    known_cards += [SushiCardType.PUDDING] * reduce(op.add, state.puddings)
    known_count = count_card_types(known_cards)
    remaining_counts = { card: count - known_count[card] for card, count in TOTAL_CARD_COUNTS.items() }
    remaining_total = TOTAL_CARDS - len(known_cards) + known_count[SushiCardType.HIDDEN]
    hidden_count = known_count[SushiCardType.HIDDEN]
    probabilities = { card: 1.0 - prob_no_picks(remaining_total,
                                                remaining_counts[card],
                                                hidden_count) for card, count in remaining_counts.items() if card != SushiCardType.HIDDEN} 
    return probabilities
