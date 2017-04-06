import pygame
from pygame.locals import *
import sys

# global constants
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 240
SCREEN_CAPTION = 'Legend of Pygame v0.5'
GAME_SCREEN_HEIGHT = 176
TILE_SIZE = 16
FPS = 60
BLACK = (0, 0, 0)
WHITE = (222, 222, 222)
GREEN = (0, 222, 0)


def main():
    """Main function to be run on start-up"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(SCREEN_CAPTION)
    game_clock = pygame.time.Clock()
    play_intro(screen)
    while True:
        #play_game(screen, game_clock)
        game_over(screen)


def play_intro(display):
    """Displays intro text, waits for input."""
    intro_font1 = pygame.font.Font('8bo.ttf', 24)
    intro_surf1 = intro_font1.render('Legend of Pygame', False, WHITE)
    intro_rect1 = intro_surf1.get_rect()
    intro_rect1.midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    intro_font2 = pygame.font.Font('8bo.ttf', 12)
    intro_surf2 = intro_font2.render('Press Enter to Begin', False, WHITE)
    intro_rect2 = intro_surf2.get_rect()
    intro_rect2.midtop = (SCREEN_WIDTH / 2, intro_rect1.bottom + 12)
    display.fill(BLACK)
    display.blit(intro_surf1, intro_rect1)
    display.blit(intro_surf2, intro_rect2)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_KP_ENTER:
                    return
                elif event.key == K_ESCAPE:
                    terminate()


def play_game(screen, game_clock):
    """Main gameplay loop."""
    game_screen = pygame.Surface((SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
    #TODO - initialize ObjectHandler, other stuff
    while True:
        if len(pygame.event.get(QUIT)) > 0:
            terminate()
        #TODO -- game loop logic (ObjectHandler, etc)
        screen.fill(BLACK)
        screen.blit(game_screen, (0, SCREEN_HEIGHT - GAME_SCREEN_HEIGHT))
        #TODO -- draw game objects, debug pane
        pygame.display.update()
        game_clock.tick(FPS)


def game_over(screen):
    """Displays game over screen, waits for input."""
    go_font = pygame.font.Font('8bo.ttf', 48)
    game_surf = go_font.render('GAME', False, WHITE)
    game_rect = game_surf.get_rect()
    game_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
    over_surf = go_font.render('OVER', False, WHITE)
    over_rect = over_surf.get_rect()
    over_rect.center = (SCREEN_WIDTH / 2, 2 * SCREEN_HEIGHT / 3)
    screen.fill(BLACK)
    screen.blit(game_surf, game_rect)
    screen.blit(over_surf, over_rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_KP_ENTER:
                    return
                elif event.key == K_ESCAPE:
                    terminate()


def terminate():
    """Exits the program when called."""
    pygame.quit()
    sys.exit()

# Run main() -- LAST LINES OF FILE
if __name__ == '__main__':
    main()
