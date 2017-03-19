import pygame, sys, json
from pygame.locals import *
import GameObjects04

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
LEVEL_FILE = 'level_data.json'


def main():
    pygame.init()
    global SCREEN, GAME_CLOCK
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('v.04')
    GAME_CLOCK = pygame.time.Clock()
    play_intro()
    SCREEN.fill(BLACK)
    while True:
        play_game()
        # game over


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
    player = GameObjects04.Player(all_objects, coords=(128, 80))
    location = 'h8'
    loc_objs, _ = load_screen(location)
    all_objects.add(loc_objs)
    while True:
        if len(pygame.event.get(QUIT)) > 0:
            terminate()
        #TODO -- move Exit collision check to Player class, get it to work (BELOW)
        for obj in all_objects:
            if isinstance(obj, GameObjects04.Exit):
                if pygame.sprite.collide_rect(obj, player):
                    screen_transition(all_objects, obj.destination, obj.direction)
                    new_objects, entry_points = load_screen(obj.destination)
                    all_objects.clear()
                    all_objects.add(new_objects)
                    player.set_coords(entry_points[obj.direction])
                    all_objects.add(player)
        # ABOVE: SEE "to do"
        player.update(all_objects)
        game_screen.fill(bg_color)
        all_objects.draw(game_screen)
        SCREEN.blit(game_screen, (0, SCREEN_HEIGHT - GAME_SCREEN_HEIGHT))
        pygame.display.update()
        GAME_CLOCK.tick(FPS)


def load_screen(name, offsetX=0, offsetY=0):
    """Takes name of screen, looks it up in the file, returns GameObjects and Entry Points"""
    with open(LEVEL_FILE, 'r') as readfile:
        all_screens = json.load(readfile)
    assert name in all_screens.keys(), 'load_screen(): Given screen name not found in level data.'
    screen = all_screens[name]
    screen_objects = []
    if 'objects' in screen.keys():
        for obj in screen['objects']:
            kw_dict = {}
            for key, value in obj.items():
                if key != 'type':
                    kw_dict[key] = value
            offset_coords = list(kw_dict['coords'])
            offset_coords[0] += offsetX
            offset_coords[1] += offsetY
            kw_dict['coords'] = offset_coords
            if obj['type'] == 'wall':
                screen_objects.append(GameObjects04.Wall(**kw_dict))
            elif obj['type'] == 'exit':
                screen_objects.append(GameObjects04.Exit(**kw_dict))
    entry_points = {}
    if 'entry_points' in screen.keys():
        entry_points = screen['entry_points']
    return screen_objects, entry_points


def screen_transition(game_screen, current_objects, destination_name, direction):
    assert direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']
    offset_horz = 0
    if direction == 'UP':
        offset_horz -= GAME_SCREEN_HEIGHT
    elif direction == 'DOWN':
        offset_horz += GAME_SCREEN_HEIGHT
    offset_vert = 0
    if direction == 'LEFT':
        offset_vert -= SCREEN_WIDTH
    elif direction == 'RIGHT':
        offset_vert += SCREEN_WIDTH
    draw_objects = pygame.sprite.Group()
    for o in current_objects:
        if not isinstance(o, GameObjects04.Player) and not isinstance(o, GameObjects04.Exit):
            draw_objects.add(o)
    new_objects, _ = load_screen(destination_name, offsetX=offset_horz, offsetY=offset_vert)
    draw_objects.add(new_objects)
    if direction == 'UP' or direction == 'DOWN':
        for i in range(GAME_SCREEN_HEIGHT):
            for o in draw_objects:
                if direction == 'UP':
                    o.rect.top += 1
                else:
                    o.rect.top -= 1
            game_screen.fill(BLACK)
            draw_objects.draw(game_screen)
            SCREEN.blit(game_screen, (0, SCREEN_HEIGHT - GAME_SCREEN_HEIGHT))
            pygame.display.update(Rect(0, SCREEN_HEIGHT - GAME_SCREEN_HEIGHT, SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
    else:
        for i in range(SCREEN_WIDTH):
            for o in draw_objects:
                if direction == 'LEFT':
                    o.rect.left -= 1
                else:
                    o.rect.left += 1
            game_screen.fill(BLACK)
            draw_objects.draw(game_screen)
            SCREEN.blit(game_screen, (0, SCREEN_HEIGHT - GAME_SCREEN_HEIGHT))
            pygame.display.update(Rect(0, SCREEN_HEIGHT - GAME_SCREEN_HEIGHT, SCREEN_WIDTH, GAME_SCREEN_HEIGHT))


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
