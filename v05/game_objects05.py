import pygame
from pygame.locals import *

class GameObject(pygame.sprite.Sprite):
    """Base class for all objects in the game."""
    def __init__(self, *sprite_groups, **kwargs):
        pygame.sprite.Sprite.__init__(self, sprite_groups)
        if 'image' in kwargs.keys():
            self.image = kwargs['image']
            self.rect = self.image.get_rect()
        if 'coords' in kwargs.keys():
            self.rect.topleft = kwargs['coords']
        if 'dx' in kwargs.keys():
            self.dx = kwargs['dx']
        else:
            self.dx = 0
        if 'dy' in kwargs.keys():
            self.dy = kwargs['dy']
        else:
            self.dy = 0

    def update(self):
        self.rect.left += self.dx
        self.rect.top += self.dy

class Wall(GameObject):
    """Class for all impassable objects."""
    def __init__(self, *sprite_groups, **kwargs):
        GameObject.__init__(self, sprite_groups, kwargs)

class ObjectHandler:
    """Class for all game sprite operations (collision, drawing, etc)"""
    def __init__(self):
        self.player_objects = pygame.sprite.OrderedUpdates()
        self.enemy_objects = pygame.sprite.Group()
        self.wall_objects = pygame.sprite.Group()
        self.other_objects = pygame.sprite.Group()
        # TODO -- added structure for screen transitions

    def draw(self, display):
        for group in self.all_groups():
            group.draw(display)

    def all_groups(self):
        return [self.player_objects, self.enemy_objects, self.wall_objects, self.other_objects]

    def load_screen(self, screen_data, **kwargs):
        # TODO -- loading objects (x/y offset in kwargs for screen transitions)
        pass
