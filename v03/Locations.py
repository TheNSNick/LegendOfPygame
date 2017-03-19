import pygame, json
from pygame.locals import *
import GameObjects


class Location():

    def __init__(self, **kwargs):
        self.name = ''
        self.objects = []

    def __iter__(self):
        return self.objects.__iter__()

    def __len__(self):
        return self.objects.__len__()

    def add_object(self, game_object):
        assert isinstance(game_object, GameObjects.GameObject), 'Non GameObject passed to Location.add_object()'
        self.objects.append(game_object)

    def load_objects(self, location_data):
        if 'walls' in location_data.keys():
            walls = location_data['walls']
            for obj in walls:
                obj_image = pygame.Surface((obj['width'], obj['height']))
                obj_image.fill(obj['color'])
                self.add_object(GameObjects.Wall(image=obj_image, coords=obj['coords']))

    def load_screen(self, level_file, location_name):
        self.name = location_name
        with open(level_file, 'r') as readfile:
            level_data = json.load(readfile)
            location_data = level_data[location_name]
            self.load_objects(location_data)
