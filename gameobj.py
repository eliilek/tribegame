import pygame
from pygame.locals import *

class GameObj:
    def __init__(self):
        self._visible = False
        self.display_surf = None
        self.image = None
        self.image_rect = None

    def init_to_draw(self, display_surf, image, pos, rect = None):
        self.display_surf = display_surf
        self.image = image
        self.image_rect = rect
        self.pos = pos
        self._visible = True

    def loop(self):
        pass

    def render(self):
        pass
