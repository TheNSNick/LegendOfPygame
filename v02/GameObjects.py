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

    def set_coords(self, coords):
        self.rect.topleft = coords

    def set_image(self, image):
        self.image = image
        old_center = self.rect.center
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        self.rect.center = old_center

    def update(self, *args, **kwargs):
        pass


class Player(Game_Object):
    """Class representing the player sprite."""

    def __init__(self, *args, **kwargs):
        # placeholder player image
        player_image = pygame.Surface((16, 16))
        player_image.fill((0, 222, 0))
        kwargs['image'] = player_image
        # end placeholder image
        Game_Object.__init__(self, *args, **kwargs)
