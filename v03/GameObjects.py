import pygame
from pygame.locals import *
from game import TILE_SIZE, terminate


class GameObject(pygame.sprite.Sprite):
    """Base class for all on-screen game objects."""

    def __init__(self, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self, *args)
        self.image = pygame.Surface((0, 0))
        self.rect = Rect(0, 0, 0, 0)
        if 'image' in kwargs.keys():
            self.set_image(kwargs['image'])
        if 'coords' in kwargs.keys():
            self.set_coords(kwargs['coords'])
        if 'dx' in kwargs.keys():
            self.dx = kwargs['dx']
        else:
            self.dx = 0
        if 'dy' in kwargs.keys():
            self.dy = kwargs['dy']
        else:
            self.dy = 0

    def set_coords(self, coords):
        self.rect.topleft = coords

    def set_image(self, image):
        self.image = image
        old_center = self.rect.center
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        self.rect.center = old_center

    def update(self, *args, **kwargs):
        self.rect.left += self.dx
        self.rect.top += self.dy
        if 'coords' in kwargs.keys():
            self.rect.topleft = kwargs['coords']


class Player(GameObject):
    """Class representing the player sprite."""
    move_speed = 2

    def __init__(self, *args, **kwargs):
        GameObject.__init__(self, *args, **kwargs)
        self.spritesheet = pygame.image.load('player_sprite.png').convert()
        self.direction = ''
        self.set_direction('DOWN')

    def set_direction(self, direction):
        x_dict = {'UP': 0, 'DOWN': 1, 'LEFT': 2, 'RIGHT': 3}
        new_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        new_image.blit(self.spritesheet, (0, 0), Rect(x_dict[direction] * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
        self.set_image(new_image)
        self.direction = direction

    def process_keys(self):
        for event in pygame.event.get(KEYDOWN):
            if event.key == K_w or event.key == K_UP:
                self.set_direction('UP')
                self.dx = 0
                self.dy -= self.move_speed
            if event.key == K_s or event.key == K_DOWN:
                self.set_direction('DOWN')
                self.dx = 0
                self.dy += self.move_speed
            if event.key == K_a or event.key == K_LEFT:
                self.set_direction('LEFT')
                self.dx -= self.move_speed
                self.dy = 0
            if event.key == K_d or event.key == K_RIGHT:
                self.set_direction('RIGHT')
                self.dx += self.move_speed
                self.dy = 0
            if event.key == K_ESCAPE:
                terminate()

        for event in pygame.event.get(KEYUP):
            if (event.key == K_w or event.key == K_UP) and self.dy < 0:
                self.dy += min(-self.dy, self.move_speed)
            if (event.key == K_s or event.key == K_DOWN) and self.dy > 0:
                self.dy -= min(self.dy, self.move_speed)
            if (event.key == K_a or event.key == K_LEFT) and self.dx < 0:
                self.dx += min(-self.dx, self.move_speed)
            if (event.key == K_d or event.key == K_RIGHT) and self.dx > 0:
                self.dx -= min(self.dx, self.move_speed)

    def horizontal_collisions(self, wall_group):
        walls = pygame.sprite.spritecollide(self, wall_group, False)
        while len(walls) > 0:
            if self.dx < 0:
                self.rect.left = max(wall.rect.right for wall in walls)
            elif self.dx > 0:
                self.rect.right = min(wall.rect.left for wall in walls)
            else:
                average_wall_midpoint = sum(wall.rect.centerx for wall in walls) / len(walls)
                if self.rect.centerx >= average_wall_midpoint:
                    self.rect.left = max(wall.rect.right for wall in walls)
                else:
                    self.rect.right = min(wall.rect.left for wall in walls)
            walls = pygame.sprite.spritecollide(self, wall_group, False)
            self.dx = 0

    def vertical_collisions(self, wall_group):
        walls = pygame.sprite.spritecollide(self, wall_group, False)
        while len(walls) > 0:
            if self.dy < 0:
                self.rect.top = max(wall.rect.bottom for wall in walls)
            elif self.dx > 0:
                self.rect.bottom = min(wall.rect.top for wall in walls)
            else:
                average_wall_midpoint = sum(wall.rect.centery for wall in walls) / len(walls)
                if self.rect.centery >= average_wall_midpoint:
                    self.rect.top = max(wall.rect.bottom for wall in walls)
                else:
                    self.rect.bottom = min(wall.rect.top for wall in walls)
            walls = pygame.sprite.spritecollide(self, wall_group, False)
            self.dy = 0

    def collision_check(self, objects):
        wall_group = [x for x in objects if isinstance(x, Wall)]
        if self.dx != 0 or self.dy == 0:
            self.horizontal_collisions(wall_group)
        if self.dy != 0:
            self.vertical_collisions(wall_group)

    def update(self, objects, **kwargs):
        self.process_keys()
        GameObject.update(self, **kwargs)
        self.collision_check(objects)


class Wall(GameObject):
    """Class for walls."""

    def __init__(self, *args, **kwargs):
        GameObject.__init__(self, *args, **kwargs)


class Door(GameObject):
    """Class for Game Objects that take the Player to another location."""

    def __init__(self, *args, **kwargs):
        GameObject.__init__(self, *args, **kwargs)
        self.location = kwargs['location']
        if 'transition' in kwargs.keys():
            self.transition = kwargs['transition']
        else:
            self.transition = 'OTHER'
        if 'points' in kwargs.keys():
            self.trigger_points = kwargs['points']
        else:
            self.trigger_points = [self.rect.top, self.rect.bottom, self.rect.left, self.rect.right]


class Enemy(GameObject):
    """Base class for enemies."""

    def __init__(self, *args, **kwargs):
        GameObject.__init__(self, *args, **kwargs)
        #TODO
