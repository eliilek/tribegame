import pygame
import random

class TileManager(object):
    def __init__(self, size, tiles, camera_width, camera_height):
        self.progenitor_tiles = tiles
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.tile_size = tiles[0].image.get_rect()
        self.tiles = [[random.choice(self._progenitor_tiles).clone(i, j) for i in range(size)] for j in range(size)]
        self.village_x = random.randint(1, size - 2)
        self.village_y = random.randint(1, size - 2)
        self.tiles[self.village_x][self.village_y].to_village(1)
        for i in range(self.village_x - 1, self.village_x + 2):
            for j in range(self.village_y - 1, self.village_y + 2):
                self.tiles[i][j].reachable = True
        self.camera_center = (self.village_x * self.tile_size.width, self.village_y * self.tile_size.height)
        self.camera_x = self.camera_center[0] - (self.camera_width/2)
        self.camera_y = self.camera_center[1] - (self.camera_height/2)
        self.background_screen = pygame.Surface((size * self.tile_size.width, size * self.tile_size.height))
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles)):
                self.tiles[i][j].render(self.background_screen, i * self.tile_size.width, j * self.tile_size.height)
        self.renderable_screen = self.background_screen.copy()

    def render(self, screen, x, y):
        screen.blit(self.renderable_screen, (x, y), Rect((self.camera_x, self.camera_y), (self.camera_width, self.camera_height)))
