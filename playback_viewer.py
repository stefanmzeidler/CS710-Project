#! /usr/bin/env python3

import argparse
from sushi_state import GameState, GameStateSet, SushiCardType, count_card_types, pair_wasabi

from typing import TextIO, Tuple, List

import pygame

#from pygame.locals import *
from pygame.constants import *
from pygame.rect import Rect
from pygame.color import Color

 
class App:
    def __init__(self, turns: GameStateSet):
        self.turns = turns
        self.cur_turn = 0
        self._running = True
        self._display_surf = None
        self.clock = pygame.time.Clock()
        self.size = self.weight, self.height = 1200, 1000
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.cur_turn -= 1
                self.cur_turn %= len(self.turns.states)
                self.draw_turn()
            elif event.key == pygame.K_RIGHT:
                self.cur_turn += 1
                self.cur_turn %= len(self.turns.states)
                self.draw_turn()
                

    def on_loop(self):
        pass
    def on_render(self):
        pygame.display.flip()        

    def on_cleanup(self):
        pygame.quit()
 

    def draw_turn(self):

        self._display_surf.fill((0, 0, 0))

        state = self.turns.states[self.cur_turn]
        PLAYER_SPACING = 20
        PLAYER_W = 1200
        PLAYER_H = 400
        num_players = len(state.hands)
        for i in range(num_players):
            #self.draw_centered_text()
            y = i * (PLAYER_SPACING + PLAYER_H)
            self.draw_Player(self._display_surf.subsurface(Rect(0, y, 1200, PLAYER_H)), state, i)


    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        self.draw_turn()
        
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

            self.clock.tick(60)
        self.on_cleanup()

    @staticmethod
    def draw_centered_text(surface: pygame.Surface, x: int, y: int, msg: str, color: Color, size: int):
        font = pygame.font.Font(None, size)
        text = font.render(msg, True, color)
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)



    @staticmethod
    def draw_Player(surface: pygame.Surface, state: GameState, player_idx: int):
        
        CARD_SPACING = 5

        CARD_W = int((surface.get_width() + CARD_SPACING) / 11) 
        CARD_H = int(surface.get_height() / 3)
        FORE_C = Color('RED')
        BACK_C = Color('BLUE')
        LABEL_SIZE = 24

        y = 10
        App.draw_centered_text(surface, surface.get_width() / 2, y, f'Player {player_idx + 1}', FORE_C, LABEL_SIZE)
        
        y += 20
        App.draw_centered_text(surface, surface.get_width() / 2, y, 'Hand', FORE_C, LABEL_SIZE)
        counts = count_card_types(state.hands[player_idx])
        counts = { card:count for card, count in counts.items() if count > 0 }
        y += 10
        for k, card in enumerate(counts):
            count = counts[card]
            x = k * (CARD_W + CARD_SPACING)
            App.draw_card(surface.subsurface(Rect(x, y, CARD_W, CARD_H)), card, FORE_C, BACK_C, count)
        
        y += CARD_H + 10
        App.draw_centered_text(surface, surface.get_width() / 2, y, 'Played', FORE_C, LABEL_SIZE)
        played_cards = list(state.played_cards[player_idx])
        wasabi_combos = pair_wasabi(played_cards)
        for card in wasabi_combos:
            played_cards.remove(card)
            played_cards.remove(SushiCardType.WASABI)
        counts = count_card_types(played_cards)
        counts = { card:count for card, count in counts.items() if count > 0 }
        y += 10
        for k, card in enumerate(counts):
            count = counts[card]
            x = k * (CARD_W + CARD_SPACING)
            App.draw_card(surface.subsurface(Rect(x, y, CARD_W, CARD_H)), card, FORE_C, BACK_C, count)
        for k, card in enumerate(wasabi_combos):
            x = (k + len(counts)) * (CARD_W + CARD_SPACING)
            App.draw_card(surface.subsurface(Rect(x, y, CARD_W, CARD_H)), card, FORE_C, BACK_C, 1, True)
        
        y += CARD_H + 10
        pudding = state.puddings[player_idx]
        score = state.scores[player_idx]
        App.draw_centered_text(surface, surface.get_width() / 2, y, f'Pudding: {pudding}    Score: {score}', FORE_C, LABEL_SIZE)



    @staticmethod
    def draw_card(surface: pygame.Surface, card: SushiCardType, color_fore: Color, color_back: Color, num: int = 1, wasabi: bool = False):
        OFFSET = 0.03
        BORDER_SIZE = 2
        if wasabi:
            num = 2
        offset = max(OFFSET * surface.get_width(), OFFSET * surface.get_height())
        h = surface.get_height() - offset * (num -1)
        w = surface.get_width() - offset * (num -1)
            
        for i in range(num):
            x = int(offset * i)
            y = int(offset * i)
            pygame.draw.rect(surface, color_back, Rect(x, y, w, h))
            pygame.draw.rect(surface, color_fore, Rect(x, y, w, h), BORDER_SIZE)

        App.draw_centered_text(surface, w/2 + x, h/2 + y, card, color_fore, 14)
        if wasabi:
            App.draw_centered_text(surface, w/2 + x, h/2 + y + 15, 'with WASABI', color_fore, 14)
        else:
            App.draw_centered_text(surface, w/2 + x, h/2 + y + 15, f'x{num}', color_fore, 14)
 

def main(playback_file: TextIO):
    turns = GameStateSet.parse_raw(playback_file.read())
    theApp = App(turns)
    theApp.on_execute()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="View turns from a game playback JSON file")
    parser.add_argument(
        'play_file', type=argparse.FileType('r'),
         help='The file to open')
    args = parser.parse_args()
    main(args.play_file)
