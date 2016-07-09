import pygame
import random
from pygame.locals import *

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
        camera_center = (self.village_x * self.tile_size.width, self.village_y * self.tile_size.height)
        self.camera_x = camera_center[0] - (self.camera_width/2)
        self.camera_y = camera_center[1] - (self.camera_height/2)
        self.background_screen = pygame.Surface((size * self.tile_size.width, size * self.tile_size.height))
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles)):
                self.tiles[i][j].render(self.background_screen, i * self.tile_size.width, j * self.tile_size.height)
        self.renderable_screen = self.background_screen.copy()
        self.open_menus = []
        self.scrolling = []

    def render(self, screen, x=0, y=0):
        if len(self.scrolling) != 0:
            for direction in self.scrolling:
                self.scroll(direction)
        screen.blit(self.renderable_screen, (x, y), Rect((self.camera_x, self.camera_y), (self.camera_width, self.camera_height)))

    def click(self, mpos):
        for menu in open_menus:
            if menu.is_my_click(mpos):
                menu.click(mpos)
                break
        else:
            tile_x = (mpos[0] + self.camera_x)/self.tile_size.width
            tile_y = (mpos[1] + self.camera_y)/self.tile_size.height
            clicked_tile = self.tiles[tile_x, tile_y]
            ###Display jobs menu from clicked_tile.available_jobs
            ###Account for None jobs

    def key_down(self, key):
        if key == K_UP:
            self.scrolling.append("up")
        elif key == K_DOWN:
            self.scrolling.append("down")
        elif key == K_LEFT:
            self.scrolling.append("left")
        else:
            self.scrolling.append("right")

    def key_up(self, key):
        try:
            if key == K_UP:
                self.scrolling.remove("up")
            elif key == K_DOWN:
                self.scrolling.remove("down")
            elif key == K_LEFT:
                self.scrolling.remove("left")
            else:
                self.scrolling.remove("right")
        except:
            pass

    def scroll(self, direction):
        if direction == "up":
            self.camera_y -= 10
            if self.camera_y < 0:
                self.camera_y = 0
        elif direction == "down":
            self.camera_y += 10
            if self.camera_y > self.renderable_screen.get_height() - self.camera_height:
                self.camera_y = self.renderable_screen.get_height() - self.camera_height
        elif direction == "left":
            self.camera_x -= 10
            if self.camera_x < 0:
                self.camera_x = 0
        else:
            self.camera_x += 10
            if self.camera_x > self.renderable_screen.get_width() - self.camera_width:
                self.camera_x = self.renderable_screen.get_width() - self.camera_width
