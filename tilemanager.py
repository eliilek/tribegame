import pygame
import random

class TileManager(object):
    def __init__(self, size, tiles):
        land = [[None]*size for i in range(size)]
        for row in land:
            for tile in row:
                tile = random.choice(tiles).clone
        village_x = random.randint(1, size - 2)
        village_y = random.randint(1, size - 2)
        land[village_x][village_y].to_village(1)
