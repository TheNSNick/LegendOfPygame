import pygame

SCREEN_WIDTH = 256
DEBUG_SCREEN_HEIGHT = 64
pygame.init()
pygame.font.init()
DEBUG_FONT = pygame.font.Font('8bo.ttf', 8)
P_LOC_COORDS = (16, 4)
P_HP_COORDS = (16, 16)
P_DIR_COORDS = (16, 28)
P_MODE_COORDS = (16, 40)
LOC_NAME_COORDS = (240, 16)


class DebugPane(pygame.Surface):
    """Displays information at the top of the screen."""
    def __init__(self):
        pygame.Surface.__init__(self, (SCREEN_WIDTH, DEBUG_SCREEN_HEIGHT))

    def write(self, text, coords, **kwargs):
        text_surf = DEBUG_FONT.render(text, False, (222, 222, 222))
        text_rect = text_surf.get_rect()
        text_rect.topleft = coords
        if 'align' in kwargs.keys():
            if kwargs['align'] == 'topright':
                text_rect.topright = coords
        self.blit(text_surf, text_rect)

    def draw(self, display, player, location):
        self.fill((0, 0, 0))
        self.write('p_loc: {}'.format(player.rect.topleft), P_LOC_COORDS)
        self.write('p_health: {}'.format(player.health), P_HP_COORDS)
        self.write('p_dir: {}'.format(player.direction), P_DIR_COORDS)
        self.write('p_mode: {}'.format(player.mode), P_MODE_COORDS)
        self.write('loc: {}'.format(location), LOC_NAME_COORDS, align='topright')
        display.blit(self, (0, 0))
