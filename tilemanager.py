import pygame
import random

class TileManager(object):
    def __init__(self, size, tiles):
        self.land = [[random.choice(tiles).clone() for i in range(size)] for i in range(size)]
        self.village_x = random.randint(1, size - 2)
        self.village_y = random.randint(1, size - 2)
        self.land[self.village_x][self.village_y].to_village(1)
        for i in range(self.village_x - 1, self.village_x + 2):
            for j in range(self.village_y - 1, self.village_y + 2):
                self.land[i][j].reachable = True
