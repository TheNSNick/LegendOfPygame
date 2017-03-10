import pygame
from pygame.locals import *
from lop import *


class GameObject(pygame.sprite.Sprite):
    """Base class to be inherited by all on-screen game objects"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.dx = 0
        self.dy = 0

    def set_image(self, new_image):
        self.image = new_image
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def set_coords(self, new_coords):
        self.rect.topleft = new_coords

    def update(self):
        self.rect.left += self.dx
        self.rect.top += self.dy


class Player(GameObject):
    """Player class"""
    def __init__(self, coords=None):
        GameObject.__init__(self)
        # placeholder image - green box
        image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        image.fill((0, 222, 0))
        self.set_image(image)
        # end placeholders
        if coords:
            self.set_coords(coords)
        self.health = 6  # in half-hearts
        self.direction = 'UP'
        self.iframes = 0

    def update(self):
        GameObject.update(self)
        if self.iframes > 0:
            self.iframes -= 1

    def move(self, direction):
        self.direction = direction
        if self.direction == 'UP':
            self.dx = 0
            self.dy = -1
        elif self.direction == 'DOWN':
            self.dx = 0
            self.dy = 1
        elif self.direction == 'LEFT':
            self.dx = -1
            self.dy = 0
        elif self.direction == 'RIGHT':
            self.dx = 1
            self.dy = 0
        else:
            raise ValueError('Invalid direction -- Player.move()')


class Wall(GameObject):
    """Base wall class"""
    def __init__(self, image=None):
        GameObject.__init__(self)
        # placeholder image
        if not image:
            image = pygame.Surface((self.rect.width, self.rect.height))
            image.fill((128, 128, 128))
        # end placeholder
        self.set_image(image)


class Enemy(GameObject):
    """Base enemy class"""
    def __init__(self):
        GameObject.__init__(self)

