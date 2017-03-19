import pygame, sys
from pygame.locals import *
import GameObjects, Locations
import debug

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
    pygame.display.set_caption('rough working prototype')
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
    #TODO -- load player and location(s) from file
    player = GameObjects.Player(all_objects, coords=(128, 80))
    debug_screen = debug.DebugPane(player)
    '''# TEST LOCATIONS CONSTRUCTED BELOW
    v_wall_image = pygame.Surface((TILE_SIZE, GAME_SCREEN_HEIGHT))
    h_wall_image_full = pygame.Surface((SCREEN_WIDTH - 2 * TILE_SIZE, TILE_SIZE))
    h_wall_image_half = pygame.Surface((SCREEN_WIDTH / 2 - TILE_SIZE, TILE_SIZE))
    left_wall = GameObjects.Wall(image=v_wall_image, coords=(0,0))
    right_wall = GameObjects.Wall(image=v_wall_image, coords=(SCREEN_WIDTH - TILE_SIZE, 0))
    bottom_wall = GameObjects.Wall(image=h_wall_image_full, coords=(TILE_SIZE, GAME_SCREEN_HEIGHT - TILE_SIZE))
    top_left_wall = GameObjects.Wall(image=h_wall_image_half, coords=(0, 0))
    top_right_wall = GameObjects.Wall(image=h_wall_image_half, coords=(SCREEN_WIDTH / 2 + TILE_SIZE, 0))
    test_loc_1 = [left_wall, right_wall, bottom_wall, top_left_wall, top_right_wall]
    for wall in test_loc_1:
        wall.image.fill((128, 128, 128))
    #test_loc_2 =
    all_objects.add(test_loc_1)
    # TEST LOCATIONS CONSTRUCTED ABOVE'''
    current_screen = Locations.Location()
    current_screen.load_screen('level01.json', 'home')
    for obj in current_screen:
        all_objects.add(obj)
    while True:
        if len(pygame.event.get(QUIT)):
            terminate()
        # TESTING
        if player.rect.centery <= 0 and current_screen.name == 'home':
            new_objects = change_location(game_screen, all_objects, 'UP', 'level01.json', 'other')
            all_objects.empty()
            all_objects.add(new_objects)
            player.set_coords((120, GAME_SCREEN_HEIGHT - TILE_SIZE))
            all_objects.add(player)
            current_screen.name = 'other'
        elif player.rect.centery > GAME_SCREEN_HEIGHT and current_screen.name == 'other':
            new_objects = change_location(game_screen, all_objects, 'DOWN', 'level01.json', 'home')
            all_objects.empty()
            all_objects.add(new_objects)
            player.set_coords((120, 0))
            all_objects.add(player)
            current_screen.name = 'home'
        # END TESTING
        #TODO -- check for game over (return if so)
        game_screen.fill(bg_color)
        player.update(all_objects)
        #TODO -- update objects by group (enemies, ....?)
        all_objects.draw(game_screen)
        SCREEN.blit(game_screen, (0, SCREEN_HEIGHT - GAME_SCREEN_HEIGHT))
        debug_screen.update(player)
        debug_screen.draw(SCREEN)
        pygame.display.update()
        GAME_CLOCK.tick(FPS)


def change_location(game_screen, current_objects, direction, location_file, location_name):
    new_screen = Locations.Location()
    new_screen.load_screen(location_file, location_name)
    movement_dict = {'UP': (1, -SCREEN_HEIGHT), 'DOWN': (1, SCREEN_HEIGHT),
                     'LEFT': (0, -SCREEN_WIDTH), 'RIGHT': (0, SCREEN_WIDTH)}
    move_index, move_amount = movement_dict[direction]
    draw_objects = current_objects
    for obj in draw_objects:
        if isinstance(obj, GameObjects.Player):
            draw_objects.remove(obj)
    for obj in new_screen:
        new_coords = list(obj.rect.topleft)
        new_coords[move_index] += move_amount
        obj.set_coords(tuple(new_coords))
        draw_objects.add(obj)
    #TODO -- player movement
    if move_index == 1:
        for i in xrange(SCREEN_HEIGHT):
            for obj in draw_objects:
                if direction == 'UP':
                    obj.rect.top += 1
                elif direction == 'DOWN':
                    obj.rect.top -= 1
            game_screen.fill(BLACK)
            draw_objects.draw(game_screen)
            SCREEN.blit(game_screen, (0, SCREEN_HEIGHT - GAME_SCREEN_HEIGHT))
            pygame.display.update(Rect(0, SCREEN_HEIGHT - GAME_SCREEN_HEIGHT, SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
            GAME_CLOCK.tick(FPS)
    elif move_index == 0:
        for i in xrange(SCREEN_WIDTH):
            for obj in draw_objects:
                if direction == 'LEFT':
                    obj.rect.left += 1
                elif direction == 'RIGHT':
                    obj.rect.left -= 1
            game_screen.fill(BLACK)
            draw_objects.draw(game_screen)
            SCREEN.blit(game_screen, (0, SCREEN_HEIGHT - GAME_SCREEN_HEIGHT))
            pygame.display.update(Rect(0, SCREEN_HEIGHT - GAME_SCREEN_HEIGHT, SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
            GAME_CLOCK.tick(FPS)
    return new_screen.objects


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()