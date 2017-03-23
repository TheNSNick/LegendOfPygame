import pygame
from pygame.locals import *
from game04 import TILE_SIZE, terminate


class GameObject(pygame.sprite.Sprite):
    """Base class for objects appearing in-game."""
    def __init__(self, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self, *args)
        self.image = pygame.Surface((0, 0))
        self.rect = Rect(0, 0, 0, 0)
        if 'image' in kwargs.keys():
            self.set_image(kwargs['image'])
        elif 'color' in kwargs.keys():
            if 'size' in kwargs.keys():
                new_image = pygame.Surface(kwargs['size'])
            elif 'height' in kwargs.keys() and 'width' in kwargs.keys():
                new_image = pygame.Surface((kwargs['width'], kwargs['height']))
            new_image.fill(kwargs['color'])
            self.set_image(new_image)
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
            self.set_coords(kwargs['coords'])


class Wall(GameObject):
    """Class for impenetrable objects."""
    def __init__(self, *args, **kwargs):
        # default grey
        GameObject.__init__(self, *args, **kwargs)


class Exit(GameObject):
    """Class for transporting the player from one screen to another when contacted."""
    def __init__(self, *args, **kwargs):
        GameObject.__init__(self, *args, **kwargs)
        self.destination = kwargs['destination']
        self.direction = kwargs['direction']


class PlayerAttack(GameObject):
    """Class representing attacks that harm enemies."""
    def __init__(self, **kwargs):
        GameObject.__init__(self, **kwargs)
        self.damage = 0
        if 'damage' in kwargs.keys():
            self.damage = int(kwargs['damage'])


class SwordAttack(PlayerAttack):
    """Class representing the basic sword object."""
    width = 6
    beginning_length = 8
    extend_length = 24
    hold_frames = 12

    def __init__(self, direction, p_center, **kwargs):
        self.direction = direction
        # placeholder image
        if self.horizontal():
            image = pygame.Surface((self.beginning_length, self.width))
        else:
            image = pygame.Surface((self.width, self.beginning_length))
        image.fill((0, 0, 222))
        kw_dict = kwargs
        kw_dict['image'] = image
        # end placeholder image
        PlayerAttack.__init__(self, **kw_dict)
        self.coords = p_center
        self.align()
        self.mode = 'extend'
        self.hold_frame = 0

    def align(self):
        if self.direction == 'UP':
            self.rect.bottomleft = self.coords
        elif self.direction == 'DOWN':
            self.rect.topright = self.coords
        elif self.direction == 'LEFT':
            self.rect.bottomright = self.coords
        elif self.direction == 'RIGHT':
            self.rect.topleft = self.coords

    def horizontal(self):
        if self.direction in ['UP', 'DOWN']:
            return False
        elif self.direction in ['LEFT', 'RIGHT']:
            return True
        else:
            raise ValueError('SwordAttack.horizontal(): self.direction')

    def update(self):
        if self.mode == 'extend':
            if self.horizontal():
                new_image = pygame.Surface((self.image.get_width() + 1, self.image.get_height()))
                if new_image.get_width() >= self.extend_length:
                    self.mode = 'hold'
            else:
                new_image = pygame.Surface((self.image.get_width(), self.image.get_height() + 1))
                if new_image.get_height() >= self.extend_length:
                    self.mode = 'hold'
            new_image.fill((0, 0, 222))
            self.set_image(new_image)
            self.align()
        elif self.mode == 'hold':
            self.hold_frame += 1
            if self.hold_frame >= self.hold_frames:
                self.mode = 'retract'
                self.hold_frame = 0
        elif self.mode == 'retract':
            if self.horizontal():
                new_image = pygame.Surface((self.image.get_width() - 1, self.image.get_height()))
                if new_image.get_width() <= self.beginning_length:
                    self.kill()
            else:
                new_image = pygame.Surface((self.image.get_width(), self.image.get_height() - 1))
                if new_image.get_height() <= self.beginning_length:
                    self.kill()
            new_image.fill((0, 0, 222))
            self.set_image(new_image)
            self.align()


class Player(GameObject):
    """Class representing the player."""
    def __init__(self, *args, **kwargs):
        GameObject.__init__(self, *args, **kwargs)
        self.spritesheet = pygame.image.load('player_sprite.png').convert()
        self.direction = ''
        self.set_direction('DOWN')
        self.mode = 'move'
        self.move_speed = 2
        self.health = 6

    def set_direction(self, direction):
        x_dict = {'UP': 0, 'DOWN': 1, 'LEFT': 2, 'RIGHT': 3}
        new_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        new_image.blit(self.spritesheet, (0, 0), Rect(x_dict[direction] * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
        self.set_image(new_image)
        self.direction = direction

    def process_keys(self, object_group):
        for event in pygame.event.get(KEYDOWN):
            if self.mode == 'move':
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
                if event.key == K_z or event.key == K_RETURN:
                    self.mode = 'attack'
                    self.dx = 0
                    self.dy = 0
                    attack = SwordAttack(self.direction, self.rect.center)
                    attack.rect.center = self.rect.center
                    object_group.add(attack)
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
        if self.mode == 'attack':
            sword_out = False
            for obj in objects:
                if isinstance(obj, SwordAttack):
                    sword_out = True
            if not sword_out:
                self.mode = 'move'
        self.process_keys(objects)
        GameObject.update(self, **kwargs)
        self.collision_check(objects)
