import gameobj.py
import pygame
from pygame.locals import *

class Villager(GameObj):
    def __init__(self, name, xp_per_level):
        self.name = name
        self.xp_per_level = xp_per_level
        self.food_level = 2 * self.xp_per_level
        self.gather_level = 2 * self.xp_per_level
        self.fight_level = 2 * self.xp_per_level
        self.shaman_level = 2 * self.xp_per_level
        self.build_level = 2 * self.xp_per_level
        self.injury = 0
        self.job = IdleJob(self)

    def kill(self):
        self.Destroy()

    def loop(self):
        if self.job = None:
            self.job = IdleJob(self)
        self.job.loop()
