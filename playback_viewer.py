#! /usr/bin/env python3

import argparse
from sushi_state import GameState, GameStateSet

from typing import TextIO

import pygame

from pygame.locals import *
 
class App:
    def __init__(self, turns: GameStateSet):
        self.turns = turns
        self._running = True
        self._display_surf = None
        self.clock = pygame.time.Clock()
        self.size = self.weight, self.height = 640, 400
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        pass
    def on_render(self):
        pygame.display.flip()        

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        
        self._display_surf.fill((0, 0, 0))
        color = (255, 100, 0)
 
        pygame.draw.rect(self._display_surf, color, pygame.Rect(10, 10, 60, 60))
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

            self.clock.tick(60)
        self.on_cleanup()
 

def main(playback_file: TextIO):
    turns = GameStateSet.parse_raw(playback_file.read())
    theApp = App(turns)
    theApp.on_execute()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="View turns from a game playback JSON file")
    
    parser = argparse.ArgumentParser(
        description='sum the integers at the command line')
    parser.add_argument(
        'play_file', type=argparse.FileType('r'),
         help='The file to open')
    args = parser.parse_args()
    main(args.play_file)
