import pygame
from pygame.locals import *


class Game_Object(pygame.sprite.Sprite):
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


class Player(Game_Object):
    """Class representing the player sprite."""

    move_speed = 2

    def __init__(self, *args, **kwargs):
        self.direction = 'DOWN'
        # placeholder player image
        player_image = pygame.Surface((16, 16))
        player_image.fill((0, 222, 0))
        kwargs['image'] = player_image
        # end placeholder image
        Game_Object.__init__(self, *args, **kwargs)

    def process_keys(self):
        for event in pygame.event.get(KEYDOWN):
            if event.key == K_w:
                self.direction = 'UP'
                self.dx = 0
                self.dy -= self.move_speed
            if event.key == K_s:
                self.direction = 'DOWN'
                self.dx = 0
                self.dy += self.move_speed
            if event.key == K_a:
                self.direction == 'LEFT'
                self.dx -= self.move_speed
                self.dy = 0
            if event.key == K_d:
                self.direction == 'RIGHT'
                self.dx += self.move_speed
                self.dy = 0
        for event in pygame.event.get(KEYUP):
            if event.key == K_w and self.dy < 0:
                self.dy += min(-self.dy, self.move_speed)
            if event.key == K_s and self.dy > 0:
                self.dy -= min(self.dy, self.move_speed)
            if event.key == K_a and self.dx < 0:
                self.dx += min(-self.dx, self.move_speed)
            if event.key == K_d and self.dx > 0:
                self.dx -= min(self.dx, self.move_speed)

    def update(self, **kwargs):
        self.process_keys()
        Game_Object.update(self, **kwargs)
