import pygame
import GameObjects


class Location():
    """Class representing a Location, or one screen of the map."""

    def __init__(self, entry_points, game_objects):
        self.entry_points = {}
        for name, coords in entry_points:
            self.entry_points['name'] = coords
        if 'default' not in self.entry_points.keys():
            self.entry_points['default'] = entry_points[0]
        self.objects = []
        for obj in game_objects:
            self.objects.append(obj)


def test_location_1():
    vertical_wall_image = pygame.Surface((16, 240))
    vertical_wall_image.fill((128, 128, 128))
    left_wall = GameObjects.Wall(image=vertical_wall_image, coords=(0, 0))
    right_wall = GameObjects.Wall(image=vertical_wall_image, coords=(240, 0))
    horizontal_wall_image = pygame.Surface((256, 16))
    horizontal_wall_image.fill((128, 128, 128))
    bottom_wall = GameObjects.Wall(image=horizontal_wall_image, coords=(0, 160))
    return Location([('default', (120, 80)), ('top', (120, 0))], [left_wall, right_wall, bottom_wall])
