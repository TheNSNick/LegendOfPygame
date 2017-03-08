import sys, pygame
from pygame.locals import *

SCREEN = None
GAME_CLOCK = None
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 240
TILE_SIZE = 16
FPS = 60


def main():
    pygame.init()
    global SCREEN, GAME_CLOCK
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    GAME_CLOCK = pygame.time.Clock()
    play_intro()
    while True:
        run_game()
        game_over()


def play_intro():
    pass


def game_over():
    pass


def run_game():
    pass
