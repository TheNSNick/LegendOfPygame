import sys, pygame
from pygame.locals import *
from classes import *

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


def play_game(player, wall_group):
    """MAIN SECOND-TO-SECOND GAMEPLAY LOOP"""
    # update player
    player.update()
    # check for player/trigger collisions, do stuff if nec.
    # check for key-presses, do stuff if nec. (e.g. make PlayerProjectile, update Player.dx/.dy)
    process_keys(player)
    # update PlayerProjectile (if any)
    # check for PlayerProjectile/Enemy collisions
    # update Enemies
    # make Enemy Projectiles if nec.
    # check for Enemy/Player collisions
    # check for EnemyProjectile/Player collisions
    # check for Wall/Player collisions, move Player outside wall if nec.
    wall_collisions = pygame.sprite.spritecollide(player, wall_group, False)
    while len(wall_collisions) > 0:
        for wall_hit in wall_collisions:
            if player.direction == 'UP':
                player.rect.top = wall_hit.rect.bottom
            elif player.direction == 'DOWN':
                player.rect.bottom = wall_hit.rect.top
            elif player.direction == 'LEFT':
                player.rect.left = wall_hit.rect.right
            elif player.direction == 'RIGHT':
                player.rect.right = wall_hit.rect.left
        wall_collisions = pygame.sprite.spritecollide(player, wall_group, False)


def process_keys(player):
    for event in pygame.event.get(KEYDOWN):
        if event.key == K_ESCAPE:
            terminate()
        elif event.key == K_w or event.key == K_UP:
            player.move('UP')
        elif event.key == K_s or event.key == K_DOWN:
            player.move('DOWN')
        elif event.key == K_a or event.key == K_LEFT:
            player.move('LEFT')
        elif event.key == K_d or event.key == K_RIGHT:
            player.move('RIGHT')
        #elif event.key == K_[key here]:
            #player action here
    for event in pygame.event.get(KEYUP):
        if (event.key == K_w or event.key == K_s or event.key == K_UP or event.key == K_DOWN) and player.dy != 0:
            player.dy = 0
        elif (event.key == K_a or event.key == K_d or event.key == K_LEFT or event.key == K_RIGHT) and player.dx != 0:
            player.dx = 0


def play_intro():
    pass


def game_over():
    pass


def run_game():
    game_screen = pygame.Surface((256, 176))
    p = Player()
    p.set_coords((120, 136))
    player_group = pygame.sprite.Group()
    player_group.add(p)
    wall_group = pygame.sprite.Group()
    wall_group.add(load_level('samplescreen.txt'))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
        play_game(p, wall_group)
        game_screen.fill((0, 0, 0))
        player_group.draw(game_screen)
        wall_group.draw(game_screen)
        SCREEN.blit(game_screen, (0, 64))
        pygame.display.update()
        GAME_CLOCK.tick(FPS)


def load_level(level_file):
    """Takes file name, returns list of lists (array of screen tiles)"""
    objects = []
    wall_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    wall_image.fill((128, 128, 128))
    y = 0
    with open(level_file, 'r') as readfile:
        for line in readfile:
            for x in xrange(len(line)):
                if line[x] == 'X':
                    wall = Wall(image=wall_image)
                    wall.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)
                    objects.append(wall)
            y += 1
    return objects


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
