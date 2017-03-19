import json

level_dict = {'h8': {'objects': [{'type': 'wall', 'color': (128, 128, 128), 'size': (256, 16), 'coords': (0, 160)},
                                 {'type': 'wall', 'color': (128, 128, 128), 'size': (16, 144), 'coords': (0, 16)},
                                 {'type': 'wall', 'color': (128, 128, 128), 'size': (16, 144), 'coords': (240, 16)},
                                 {'type': 'wall', 'color': (128, 128, 128), 'size': (112, 16), 'coords': (0, 0)},
                                 {'type': 'wall', 'color': (128, 128, 128), 'size': (112, 16), 'coords': (144, 0)},
                                 {'type': 'exit', 'direction': 'UP', 'coords': (128, -8), 'destination': 'h7'}
                                 ],
                     'entry_points': {'DOWN': (120, 0), 'LEFT': (240, 80), 'RIGHT': (0, 80)}
                     },
              'h7': {'objects': [{'type': 'wall', 'color': (128, 128, 128), 'size': (256, 16), 'coords': (0, 0)},
                                 {'type': 'wall', 'color': (128, 128, 128), 'size': (16, 144), 'coords': (0, 16)},
                                 {'type': 'wall', 'color': (128, 128, 128), 'size': (16, 144), 'coords': (240, 16)},
                                 {'type': 'wall', 'color': (128, 128, 128), 'size': (112, 16), 'coords': (0, 160)},
                                 {'type': 'wall', 'color': (128, 128, 128), 'size': (112, 16), 'coords': (144, 160)},
                                 {'type': 'exit', 'direction': 'DOWN', 'coords': (128, 248), 'destination': 'h8'}
                                 ],
                     'entry_points': {'UP': (120, 160), 'LEFT': (240, 80), 'RIGHT': (0, 80)}
                     }
              }

with open('level_data.json', 'w') as savefile:
    json.dump(level_dict, savefile, indent=4)
