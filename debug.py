import pygame
from pygame.locals import *


class DebugPane(pygame.Surface):
    width = 256
    height = 64

    def __init__(self, player):
        pygame.Surface.__init__(self, (self.width, self.height))
        self.font = pygame.font.SysFont('lucidaconsole', 8)
        self.player_loc = (0, 0)
        #self.player_health = 0
        self.update(player)

    def draw(self, display):
        self.fill((0, 0, 0))
        loc_surf = self.font.render('P_loc: ({}, {})'.format(self.player_loc[0], self.player_loc[1]), False, (222, 222, 222))
        self.blit(loc_surf, (8, 8))
        #hp_surf = self.font.render('P_hp: {}'.format(self.player_health), False, (222, 222, 222))
        #self.blit(hp_surf, (8, 20))
        display.blit(self, (0, 0))

    def update(self, player):
        self.player_loc = player.rect.topleft
        #self.player_health = player.health
