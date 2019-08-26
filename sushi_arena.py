#! /usr/bin/env python3

import argparse
from sushi_state import get_shuffled_cards, HAND_SIZES, SushiCardType, GameState, score_round, score_pudding
from playback import GameRecorder
from typing import List, Optional, Callable, Dict
import random
import pandas as pd

import ai_rand1
import ai_rand2
import ai_pref1
import ai_minmax1

AI_TYPES: Dict[str, Callable[[GameState], List[SushiCardType]]] = {
    'rand1': ai_rand1.play_turn,
    'rand2': ai_rand2.play_turn, 
    'pref1_pudding': ai_pref1.get_play_turn(SushiCardType.PUDDING),
    'pref1_wasabi': ai_pref1.get_play_turn(SushiCardType.WASABI),
    'pref1_tempura': ai_pref1.get_play_turn(SushiCardType.TEMPURA),
    'pref1_dumpling': ai_pref1.get_play_turn(SushiCardType.DUMPLING),
    'pref1_maki3': ai_pref1.get_play_turn(SushiCardType.MAKI_ROLLS_3),
    'minmax1': ai_minmax1.play_turn,
}


def sum_lists(first: List[int], second: List[int]) -> List[int]:
    return [x + y for x, y in zip(first, second)]


def required_length(nmin: int, nmax: Optional[int]):
    class RequiredLength(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if (nmin is not None and nmin > len(values)) or (nmax is not None and nmax < len(values)):
                msg = 'argument "{f}" requires between {nmin} and {nmax} arguments'.format(
                    f=self.dest, nmin=nmin, nmax=nmax)
                raise argparse.ArgumentTypeError(msg)
            setattr(args, self.dest, values)
    return RequiredLength

# NOTE: Modifies draw_cards
def deal_hands(draw_cards:List[SushiCardType], player_count:int) -> List[List[SushiCardType]]:
    hand_size = HAND_SIZES[player_count]
    hands: List[List[SushiCardType]] = [ [] for i in range(player_count) ]
    for i in range(player_count):
        for _ in range(hand_size):
            hands[i].append(draw_cards.pop(0))
    return hands

# Players pass hands to the next higher numbered player wrapping at the top
def run_game(players: List[str], verbose: bool, save_file: Optional[str]) -> GameState:
    start_hand_size = HAND_SIZES[len(players)]
    draw_cards = get_shuffled_cards()
    state = GameState.make_empty(len(players))
    UNKNOWN_HAND = [[SushiCardType.HIDDEN] * start_hand_size]
    record = GameRecorder()
    for round_num in range(3):
        state.hands = deal_hands(draw_cards, len(players))
        state.round_num = round_num
        round_plays: List[List[SushiCardType]] = [ [] for i in range(len(players)) ]
        for turn in range(start_hand_size):
            record.save_state(state)
            for i, player in enumerate(players):
                if turn < len(players) - 1:
                    unhidden = list(state.hands)
                    state.hands[turn + 1:] = UNKNOWN_HAND * (len(players) - 1 - turn)
                played = AI_TYPES[player](state)
                if len(played) == 2:
                    if SushiCardType.CHOPSTICKS not in state.played_cards[0]:
                        raise ValueError(f'ai {player} tried to play 2 cards without chopsticks')
                elif len(played) != 1:
                    raise ValueError(f'ai {player} tried to play {len(played)} cards')
                hand_copy = list(state.hands[0])
                for played_card in played:
                    try:
                        hand_copy.remove(played_card)
                    except ValueError:
                        raise ValueError(f'ai {player} tried to play {played} with a hand of {state.hands[0]}')
                round_plays[i] = played
                if turn < len(players) - 1:
                    state.hands = unhidden
                state.rotate_all()
            for i in range(len(players)):
                for card in round_plays[i]:
                    state.hands[i].remove(card)
                    if card != SushiCardType.PUDDING:
                        state.played_cards[i].append(card)
                    else:
                        state.puddings[i] += 1
                if len(round_plays[i]) == 2:
                    state.hands[i].append(SushiCardType.CHOPSTICKS)
                    state.played_cards[i].remove(SushiCardType.CHOPSTICKS)
            state.rotate_hands()
        round_scores = score_round(state.played_cards)
        state.scores = sum_lists(round_scores, state.scores)
        if verbose:
            state.pretty_print()
        for i in range(len(players)):
            state.discard_pile += state.played_cards[i]
            state.played_cards[i] = [] 
    pudding_scores = score_pudding(state.puddings)
    state.scores = sum_lists(pudding_scores, state.scores)
    if save_file is not None:
        record.save_state(state)
        with open(save_file, 'w') as fd:
            record.write_file(fd)
    if verbose:
        state.pretty_print()
    return state
    
    


def main(players:List[str], games: int, verbose: bool, save: bool):
    scores = []
    names = [ f'{player}_{i}' for i, player in enumerate(players)]
    win_rates:Dict[str, Dict[str, int]] = {}
    for name1 in names:
        win_rates[name1] = {}
        for name2 in names:
            win_rates[name1][name2] = 0
    for i in range(games):
        save_file = None
        if save:
            save_file = f'game{i}.json'
        result = run_game(players, verbose, save_file)
        scores.append(result.scores)
        for i in range(len(players)):
            for k in range(len(players)):
                if result.scores[i] > result.scores[k]:
                    win_rates[names[i]][names[k]] += 1
    
    win_df = pd.DataFrame(win_rates) / games * 100
    
    print(win_df)
    df = pd.DataFrame(data=scores, columns=names)
    print(df.describe())



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Run a series of games between a set of AIs")
    parser.add_argument('-p', '--players', nargs='+', choices=AI_TYPES.keys(),
                        help='<Requires 2-5> AI types for players', action=required_length(2, 5), required=True)
    parser.add_argument("-n", type=int, default=100,
                        help="Number of games to run")
    parser.add_argument("-r", type=int, default=None,
                        help="Set random seed")    
    parser.add_argument("-v", action="store_true",
                        help="Print output of each round")                
    parser.add_argument("-b", action="store_true",
                        help="Save each turn action for playback")
    try:
        args = parser.parse_args()
    except argparse.ArgumentTypeError as err:
        print(err)
        exit(1)
    random.seed(args.r)
    main(args.players, args.n, args.v, args.b)
