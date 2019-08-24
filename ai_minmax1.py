from sushi_state import GameState, SushiCardType, get_shuffled_cards, count_card_types, score_dumplings
from typing import List, Dict, Tuple
from random import randint
from functools import reduce
import operator as op
import math
import ai_pref1
import ai_rand2

def _get_available(card: SushiCardType, hand_counts0: Dict[SushiCardType, int], hand_counts1: Dict[SushiCardType, int]) -> int:
    hand0_available = math.ceil(hand_counts0[SushiCardType.PUDDING] / 2.0)
    hand1_available = math.floor(hand_counts1[SushiCardType.PUDDING] / 2.0)
    return hand0_available + hand1_available

# def _get_maki( hand_counts0: Dict[SushiCardType, int], hand_counts1: Dict[SushiCardType, int],  played_counts: Dict[SushiCardType, int]) -> Tuple[int, int]:
#     count1 = _get_available(SushiCardType.MAKI_ROLLS_1, hand_counts0, hand_counts1)
#     count2 = _get_available(SushiCardType.MAKI_ROLLS_2, hand_counts0, hand_counts1)
#     count3 = _get_available(SushiCardType.MAKI_ROLLS_3, hand_counts0, hand_counts1)
#     count = count1 + count2 + count3
#     available = count1 + 2 * count2 + 3 * count3
#     current = played_counts[SushiCardType.MAKI_ROLLS_1] * 1
#     current += played_counts[SushiCardType.MAKI_ROLLS_2] * 2
#     current += played_counts[SushiCardType.MAKI_ROLLS_3] * 3
#     return current + available, count


# Assumes 2 player
def play_turn(state: GameState) -> List[SushiCardType]:
    assert(len(state.hands) == 2)

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
    

    hand_counts0 = count_card_types(hands[0])
    hand_counts1 = count_card_types(hands[1])
    play_counts0 = count_card_types(state.played_cards[0])
    play_counts1 = count_card_types(state.played_cards[1])


    # check pudding (assume scored at end of round)
    min_pudding_score = 0.0
    if SushiCardType.PUDDING in hands[0]:
        puddings1 = state.puddings[1]
        available = _get_available(SushiCardType.PUDDING, hand_counts0, hand_counts1)
        lost = _get_available(SushiCardType.PUDDING, hand_counts1, hand_counts0)
        if state.puddings[0] + available > state.puddings[1] + lost:
            min_pudding_score = 6 / available
        if state.puddings[0] + available == state.puddings[1] + lost:
            min_pudding_score = 3 / available
    
    # check sashimi
    min_sashimi_score = 0.0
    available = _get_available(SushiCardType.SASHIMI, hand_counts0, hand_counts1)
    if (play_counts0[SushiCardType.SASHIMI] % 3) + available >= 3:
        min_sashimi_score = 10.0 / (3 - (play_counts0[SushiCardType.SASHIMI] % 3))

    # check tempura
    min_tempura_score = 0.0
    available = _get_available(SushiCardType.TEMPURA, hand_counts0, hand_counts1)
    if (play_counts0[SushiCardType.TEMPURA] % 2) + available >= 2:
        min_tempura_score = 5.0 / (2 - (play_counts0[SushiCardType.TEMPURA] % 2))

    # check Maki
    min_maki_score = 0.0
    # if hand_counts0[SushiCardType.MAKI_ROLLS_1] > 0 or hand_counts0[SushiCardType.MAKI_ROLLS_2] > 0 or hand_counts0[SushiCardType.MAKI_ROLLS_3] > 0:
    #     available1 = _get_available(SushiCardType.MAKI_ROLLS_1, hand_counts0, hand_counts1)
    #     lost1 = _get_available(SushiCardType.MAKI_ROLLS_1, hand_counts1, hand_counts0)
    #     available2 = _get_available(SushiCardType.MAKI_ROLLS_2, hand_counts0, hand_counts1)
    #     lost2 = _get_available(SushiCardType.MAKI_ROLLS_2, hand_counts1, hand_counts0)
    #     available3 = _get_available(SushiCardType.MAKI_ROLLS_3, hand_counts0, hand_counts1)
    #     lost3 = _get_available(SushiCardType.MAKI_ROLLS_3, hand_counts1, hand_counts0)
    #     current = play_counts0[SushiCardType.MAKI_ROLLS_1] * 1
    #     current += play_counts0[SushiCardType.MAKI_ROLLS_2] * 2
    #     current += play_counts0[SushiCardType.MAKI_ROLLS_3] * 3
    #     theirs = play_counts1[SushiCardType.MAKI_ROLLS_1] * 1
    #     theirs += play_counts1[SushiCardType.MAKI_ROLLS_2] * 2
    #     theirs += play_counts1[SushiCardType.MAKI_ROLLS_3] * 3
    #     their_max = lost1 + lost2 * 2 + lost3 * 3 + theirs
    #     our_max = available1 + available2 * 2 + available3 * 3 + current
    #     # need 1 to get second place
    #     if current == 0 and available1 + available2 + available3 == 1:
    #         min_maki_score = 3.0
    #     elif our_max == their_max:
    #         min_maki_score = 3.0 / (available1 + available2 + available3)
    #     elif our_max > their_max:
    #         while our_max > their_max and available1 > 0:
    #             available1 -= 1
    #             lost1 +=1
    #             their_max = lost1 + lost2 * 2 + lost3 * 3 + theirs
    #             our_max = available1 + available2 * 2 + available3 * 3 + current
    #         min_maki_score = 6.0 / (available1 + available2 + available3)

    # check wasabi
    min_wasabi_score = 0.0
    if SushiCardType.WASABI in hands[0]:
        if hand_counts1[SushiCardType.SQUID_NIGIRI] > 1:
            min_wasabi_score = 9.0 / 2.0
        elif hand_counts1[SushiCardType.SALMON_NIGIRI] > 1 or (hand_counts1[SushiCardType.SQUID_NIGIRI] > 0 and hand_counts1[SushiCardType.SALMON_NIGIRI] > 0):
            min_wasabi_score = 6.0 / 2.0
        elif hand_counts1[SushiCardType.EGG_NIGIRI] > 1 or ((hand_counts1[SushiCardType.SQUID_NIGIRI] > 0 or hand_counts1[SushiCardType.SALMON_NIGIRI] > 0) and hand_counts1[SushiCardType.EGG_NIGIRI] > 0):
            min_wasabi_score = 3.0 / 2.0

    # check nigri
    min_nigri_score = 0.0
    wasabi_mult = 1.0
    if SushiCardType.WASABI in state.played_cards[0]:
        wasabi_mult = 3.0
    if hand_counts0[SushiCardType.SQUID_NIGIRI] > 0:
        min_nigri_score = wasabi_mult * 3.0
    elif hand_counts0[SushiCardType.SALMON_NIGIRI] > 0:
        min_nigri_score = wasabi_mult * 2.0
    elif hand_counts0[SushiCardType.EGG_NIGIRI] > 0:
        min_nigri_score = wasabi_mult * 1.0

    

    # check dumpling
    available = _get_available(SushiCardType.DUMPLING, hand_counts0, hand_counts1)
    min_dumpling_score = 0.0
    if available > 0:
        min_dumpling_score = (play_counts0[SushiCardType.DUMPLING] + score_dumplings(available)) / available


    max_val = max(min_dumpling_score, min_maki_score, min_nigri_score, min_pudding_score, min_sashimi_score, min_tempura_score)


    pref_card = None
    if max_val > 0:
        if max_val == min_dumpling_score:
            pref_card = SushiCardType.DUMPLING
        elif max_val == min_maki_score:
            if SushiCardType.MAKI_ROLLS_3 in state.hands[0]:
                pref_card = SushiCardType.MAKI_ROLLS_3
            elif SushiCardType.MAKI_ROLLS_2 in state.hands[0]:
                pref_card = SushiCardType.MAKI_ROLLS_2
            else:
                pref_card = SushiCardType.MAKI_ROLLS_1
        elif max_val == min_wasabi_score:
            pref_card = SushiCardType.WASABI
        elif max_val == min_nigri_score:
            if hand_counts0[SushiCardType.SQUID_NIGIRI] > 0:
                pref_card = SushiCardType.SQUID_NIGIRI
            elif hand_counts0[SushiCardType.SALMON_NIGIRI] > 0:
                pref_card = SushiCardType.SALMON_NIGIRI
            elif hand_counts0[SushiCardType.EGG_NIGIRI] > 0:
                pref_card = SushiCardType.EGG_NIGIRI
        elif max_val == min_pudding_score:
            pref_card = SushiCardType.PUDDING
        elif max_val == min_sashimi_score:
            pref_card = SushiCardType.SASHIMI
        elif max_val == min_tempura_score:
            pref_card = SushiCardType.TEMPURA

    if pref_card is not None:
        return ai_pref1.get_play_turn(pref_card)(state)
    else:
        return ai_rand2.play_turn(state)
