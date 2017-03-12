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
    move_speed = 2
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
        self.direction = 'UP'
        self.health = 6

    def update(self, enemy_group, wall_group):
        self.rect.left += self.dx
        horz_collisions = pygame.sprite.spritecollide(self, enemy_group, False)
        if len(horz_collisions) > 0:
            self.health -= 1
            if self.dx > 0:
                self.rect.right = min(horz.rect.left for horz in horz_collisions) - 8
            elif self.dx < 0:
                self.rect.left = max(horz.rect.right for horz in horz_collisions) + 8
            self.dx = 0
        horz_collisions = pygame.sprite.spritecollide(self, wall_group, False)
        if len(horz_collisions) > 0:
            if self.dx > 0:
                self.rect.right = min(horz.rect.left for horz in horz_collisions)
            elif self.dx < 0:
                self.rect.left = max(horz.rect.right for horz in horz_collisions)
            self.dx = 0
        self.rect.top += self.dy
        vert_collisions = pygame.sprite.spritecollide(self, enemy_group, False)
        if len(vert_collisions) > 0:
            self.health -= 1
            if self.dy > 0:
                self.rect.bottom = min(vert.rect.top for vert in vert_collisions) - 8
            elif self.dy < 0:
                self.rect.top = max(vert.rect.bottom for vert in vert_collisions) + 8
            self.dy = 0
        vert_collisions = pygame.sprite.spritecollide(self, wall_group, False)
        if len(vert_collisions) > 0:
            if self.dy > 0:
                self.rect.bottom = min(vert.rect.top for vert in vert_collisions)
            elif self.dy < 0:
                self.rect.top = max(vert.rect.bottom for vert in vert_collisions)
            self.dy = 0

    def move(self, direction):
        self.direction = direction
        if self.direction == 'UP':
            self.dx = 0
            self.dy = -1 * self.move_speed
        elif self.direction == 'DOWN':
            self.dx = 0
            self.dy = self.move_speed
        elif self.direction == 'LEFT':
            self.dx = -1 * self.move_speed
            self.dy = 0
        elif self.direction == 'RIGHT':
            self.dx = self.move_speed
            self.dy = 0
        else:
            raise ValueError('Invalid direction -- Player.move()')


class Wall(GameObject):
    """Base wall class"""
    def __init__(self, x, y, width, height, image=None):
        GameObject.__init__(self)
        # placeholder image
        if not image:
            image = pygame.Surface((width, height))
            image.fill((128, 128, 128))
        # end placeholder
        self.set_image(image)
        self.set_coords((x, y))


class Enemy(GameObject):
    """Base enemy class"""
    def __init__(self, x, y):
        GameObject.__init__(self)
        # placeholder image
        image = pygame.Surface((16, 16))
        image.fill((222, 0, 0))
        self.set_image(image)
        self.set_coords((x, y))

