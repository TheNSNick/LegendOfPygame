import pygame, sys
from pygame.locals import *
import GameObjects
import locations

SCREEN = None
GAME_CLOCK = None
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 240
GAME_SCREEN_HEIGHT = 176
TILE_SIZE = 16
FPS = 60
BLACK = (0, 0, 0)
WHITE = (222, 222, 222)
GREEN = (0, 222, 0)


def main():
    pygame.init()
    global SCREEN, GAME_CLOCK
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    GAME_CLOCK = pygame.time.Clock()
    play_intro()
    SCREEN.fill(BLACK)
    while True:
        play_game()
        # game_over()


def play_intro():
    intro_font1 = pygame.font.SysFont('arial', 24)
    intro_surf1 = intro_font1.render('Legend of Pygame', False, WHITE)
    intro_rect1 = intro_surf1.get_rect()
    intro_rect1.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    intro_font2 = pygame.font.SysFont('arial', 12)
    intro_surf2 = intro_font2.render('Press Enter to Begin', False, WHITE)
    intro_rect2 = intro_surf2.get_rect()
    intro_rect2.midtop = (SCREEN_WIDTH / 2, intro_rect1.bottom + 12)
    SCREEN.fill(BLACK)
    SCREEN.blit(intro_surf1, intro_rect1)
    SCREEN.blit(intro_surf2, intro_rect2)
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


def play_game():
    game_screen = pygame.Surface((SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
    bg_color = BLACK
    all_objects = pygame.sprite.Group()
    player = GameObjects.Player(all_objects, coords=(120, 80))
    # TESTING BELOW
    '''
    wall_group = pygame.sprite.Group()
    wall_image = pygame.Surface((32, 32))
    wall_image.fill((128, 128, 128))
    wall_1 = Game_Object(all_objects, wall_group, image=wall_image, coords=(50, 50))
    wall_2 = Game_Object(all_objects, wall_group, image=wall_image, coords=(98, 50))
    '''
    enter_coords, wall_group, door_group, enemy_group = load_location(locations.test_location_1())
    print 'enter_coords = {}'.format(enter_coords)
    player.set_coords(enter_coords[1])
    all_objects.add(wall_group)
    # TESTING ABOVE
    while True:
        if len(pygame.event.get(QUIT)) > 0:
            terminate()
        game_screen.fill(bg_color)
        player.update(wall_group)
        all_objects.draw(game_screen)
        SCREEN.blit(game_screen, (0, SCREEN_HEIGHT - GAME_SCREEN_HEIGHT))
        pygame.display.update()
        GAME_CLOCK.tick(FPS)


def load_location(location, **kwargs):
    """Returns location in the form of: [player_coords], [wall_group], [door group], [enemy_group]"""
    if 'entry_point' not in kwargs.keys():
        coords = location.entry_points['default']
    else:
        coords = location.entry_points[kwargs['entry_point']]
    wall_group = pygame.sprite.Group()
    door_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    for obj in location.objects:
        if isinstance(obj, GameObjects.Wall):
            wall_group.add(obj)
        if isinstance(obj, GameObjects.Door):
            door_group.add(obj)
        if isinstance(obj, GameObjects.Enemy):
            enemy_group.add(obj)
    return coords, wall_group, door_group, enemy_group


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()