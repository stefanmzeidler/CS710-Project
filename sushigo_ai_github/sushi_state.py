from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel
from enum import Enum, auto
from random import randint


class SushiCardType(str, Enum):
    TEMPURA = 'TEMPURA'
    SASHIMI = 'SASHIMI'
    DUMPLING = 'DUMPLING'
    MAKI_ROLLS_1 = 'MAKI_ROLLS_1'
    MAKI_ROLLS_2 = 'MAKI_ROLLS_2'
    MAKI_ROLLS_3 = 'MAKI_ROLLS_3'
    SALMON_NIGIRI = 'SALMON_NIGIRI'
    SQUID_NIGIRI = 'SQUID_NIGIRI'
    EGG_NIGIRI = 'EGG_NIGIRI'
    PUDDING = 'PUDDING'
    WASABI = 'WASABI'
    CHOPSTICKS = 'CHOPSTICKS'
    HIDDEN = 'HIDDEN'

TOTAL_CARD_COUNTS = {
    SushiCardType.TEMPURA: 14,
    SushiCardType.SASHIMI: 14,
    SushiCardType.DUMPLING: 14,
    SushiCardType.MAKI_ROLLS_1: 6,
    SushiCardType.MAKI_ROLLS_2: 12,
    SushiCardType.MAKI_ROLLS_3: 8,
    SushiCardType.SALMON_NIGIRI: 10,
    SushiCardType.SQUID_NIGIRI: 5,
    SushiCardType.EGG_NIGIRI: 5,
    SushiCardType.PUDDING: 10,
    SushiCardType.WASABI: 6,
    SushiCardType.CHOPSTICKS: 4,
}
TOTAL_CARDS = sum(TOTAL_CARD_COUNTS.values())

HAND_SIZES = {
    2: 10,
    3: 9,
    4: 8,
    5: 7,
}

NIGIRI_VALS = {
    SushiCardType.EGG_NIGIRI: 1,
    SushiCardType.SALMON_NIGIRI: 2,
    SushiCardType.SQUID_NIGIRI: 3,
}

def pair_wasabi(cards: List[SushiCardType]) -> List[SushiCardType]:
    pairs: List[SushiCardType] = []
    wasabi = 0
    for card in cards:
        if card == SushiCardType.WASABI:
            wasabi += 1
        elif card in NIGIRI_VALS:
            if wasabi > 0:
                wasabi -= 1
                pairs.append(card)
    return pairs

def count_card_types(cards: List[SushiCardType]) -> Dict[SushiCardType, int]:
    counts = {}
    for card in SushiCardType:
        counts[card] = 0
    for card in cards:
        counts[card] += 1
    return counts

def score_dumplings(dumplings: int) -> int:
    dumplings = min(dumplings, 5)
    return int(dumplings * (dumplings + 1) / 2)

# NOTE: modifies scores
def divide_points(scores: List[int], total:int , players_points: List[int], winning_points: Optional[int]=None):
    if winning_points is None:
        winning_points = max(players_points)
    players = [ i for i in range(len(players_points)) if players_points[i] == winning_points]
    score = int(total / len(players))
    for i in players:
        scores[i] += score

def score_round(played_cards: List[List[SushiCardType]]) -> List[int]:
    scores = [0] * len(played_cards)
    maki_counts = [0] * len(played_cards)
    for i, cards in enumerate(played_cards):
        counts = count_card_types(cards)
        scores[i] += 5 * int(counts[SushiCardType.TEMPURA] / 2)
        scores[i] += 10 * int(counts[SushiCardType.SASHIMI] / 3)
        scores[i] += score_dumplings(counts[SushiCardType.DUMPLING])
        # Score nigiri
        wasabi = 0
        for card in cards:
            if card == SushiCardType.WASABI:
                wasabi += 1
            nigiri_val = NIGIRI_VALS.get(card)
            if nigiri_val is not None:
                if wasabi > 0:
                    wasabi -= 1
                    nigiri_val *= 3
                scores[i] += nigiri_val
        maki_counts[i] += counts[SushiCardType.MAKI_ROLLS_1] * 1
        maki_counts[i] += counts[SushiCardType.MAKI_ROLLS_2] * 2
        maki_counts[i] += counts[SushiCardType.MAKI_ROLLS_3] * 3
    # Score Maki
    ordered = sorted(maki_counts)
    if ordered[-1] > 0:
        divide_points(scores, 6, maki_counts, ordered[-1])
        if ordered[-2] > 0:
            divide_points(scores, 3, maki_counts, ordered[-2])
    return scores

def score_pudding(pudding_counts: List[int]) -> List[int]:
    scores = [0] * len(pudding_counts)
    if all([pudding_counts[i] == pudding_counts[i+1] for i in range(len(pudding_counts)-1)]):
        return scores
    divide_points(scores, 6, pudding_counts)
    if len(pudding_counts) == 2:
        return scores
    min_val = min(pudding_counts)
    divide_points(scores, -6, pudding_counts, min_val)
    return scores



class GameState(BaseModel):
    discard_pile: List[SushiCardType]
    played_cards: List[List[SushiCardType]]
    hands: List[List[SushiCardType]]
    puddings: List[int]
    round_num: int
    scores: List[int]

    @classmethod
    def make_empty(cls, num_players: int):
        return cls(discard_pile=[],
                   played_cards = [ [] for i in range(num_players) ],
                   hands = [ [] for i in range(num_players) ],
                   puddings = [0] * num_players,
                   round_num = 0,
                   scores = [0] * num_players,
        )

    def rotate_all(self):
        self.hands = self.hands[1:] + self.hands[:1]
        self.played_cards = self.played_cards[1:] + self.played_cards[:1]
        self.scores = self.scores[1:] + self.scores[:1]
        self.puddings = self.puddings[1:] + self.puddings[:1]        

    def rotate_hands(self):
        self.hands = self.hands[1:] + self.hands[:1]

    def pretty_print(self):
        print(f'ROUND: {self.round_num}')
        print('DISCARD')
        for card in self.discard_pile:
            print(f'\t{card.value}')
        for i in range(len(self.played_cards)):
            print(f'PLAYER {i}')
            print(f'\tSCORE: {self.scores[i]}')
            print(f'\tPUDDINGS: {self.puddings[i]}')
            print('\tHAND')
            for card in self.hands[i]:
                print(f'\t\t{card.value}')  
            print('\tPLAYED')
            for card in self.played_cards[i]:
                print(f'\t\t{card.value}')                

class GameStateSet(BaseModel):
    states: List[GameState]

def get_shuffled_cards() -> List[SushiCardType]:
    cards: List[SushiCardType] = []
    shuffled: List[SushiCardType] = []
    for card, count in TOTAL_CARD_COUNTS.items():
        cards += [card] * count
    for i in range(TOTAL_CARDS - 1, -1, -1):
        idx = randint(0, i)
        shuffled.append(cards.pop(idx))
    return shuffled
