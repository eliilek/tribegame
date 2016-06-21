import gameobj.py
import pygame
import random
from pygame.locals import *

class Villager(GameObj):
    @property
    def food_xp(self):
        return self._food_xp
    @food_xp.setter
    def food_xp(self, x):
        self._food_xp = x
        if self._food_xp > 8 * parent.xp_per_level - 1:
            self._food_xp = 8 * parent.xp_per_level - 1
        elif self._food_xp < 0:
            self._food_xp = 0

    @property
    def gather_xp(self):
        return self._gather_xp
    @gather_xp.setter
    def gather_xp(self, x):
        self._gather_xp = x
        if self._gather_xp > 8 * parent.xp_per_level - 1:
            self._gather_xp = 8 * parent.xp_per_level - 1
        elif self._gather_xp < 0:
            self._gather_xp = 0

    @property
    def fight_xp(self):
        return self._fight_xp
    @fight_xp.setter
    def fight_xp(self, x):
        self._fight_xp = x
        if self._fight_xp > 8 * parent.xp_per_level - 1:
            self._fight_xp = 8 * parent.xp_per_level - 1
        elif self._fight_xp < 0:
            self._fight_xp = 0

    @property
    def shaman_xp(self):
        return self._shaman_xp
    @shaman_xp.setter
    def shaman_xp(self, x):
        self._shaman_xp = x
        if self._shaman_xp > 8 * parent.xp_per_level - 1:
            self._shaman_xp = 8 * parent.xp_per_level - 1
        elif self._shaman_xp < 0:
            self._shaman_xp = 0

    @property
    def build_xp(self):
        return self._build_xp
    @build_xp.setter
    def build_xp(self, x):
        self._build_xp = x
        if self._build_xp > 8 * parent.xp_per_level - 1:
            self._build_xp = 8 * parent.xp_per_level - 1
        elif self._build_xp < 0:
            self._build_xp = 0

    @property
    def injury(self):
        return self._injury
    @injury.setter
    def injury(self, x):
        self._injury = x
        if self._injury > parent.injury_threshold:
            self.kill()
        elif self._injury < 0:
            self._injury = 0

    def __init__(self, parent, name):
        GameObj.__init__(self)
        self.name = name
        self._food_xp = 2 * parent.xp_per_level
        self._gather_xp = 2 * parent.xp_per_level
        self._fight_xp = 2 * parent.xp_per_level
        self._shaman_xp = 2 * parent.xp_per_level
        self._build_xp = 2 * parent.xp_per_level
        self._injury = 0
        self.job = IdleJob(self)
        self.parent = parent

    def get_food_xp(self):
        self.food_xp += 1
        if random.randint(1, 100) <= self.parent.double_xp_chance:
            self.food_xp += 1
        if random.randint(1, 100) <= self.parent.xp_loss_chance:
            case = random.randint(1, 4)
            if case == 1:
                self.gather_xp -= 1
            elif case == 2:
                self.fight_xp -= 1
            elif case == 3:
                self.shaman_xp -= 1
            else:
                self.build_xp -= 1

    def get_gather_xp(self):
        self.gather_xp += 1
        if random.randint(1, 100) <= self.parent.double_xp_chance:
            self.gather_xp += 1
        if random.randint(1, 100) <= self.parent.xp_loss_chance:
            case = random.randint(1, 4)
            if case == 1:
                self.food_xp -= 1
            elif case == 2:
                self.fight_xp -= 1
            elif case == 3:
                self.shaman_xp -= 1
            else:
                self.build_xp -= 1

    def get_fight_xp(self):
        self.fight_xp += 1
        if random.randint(1, 100) <= self.parent.double_xp_chance:
            self.fight_xp += 1
        if random.randint(1, 100) <= self.parent.xp_loss_chance:
            case = random.randint(1, 4)
            if case == 1:
                self.food_xp -= 1
            elif case == 2:
                self.gather_xp -= 1
            elif case == 3:
                self.shaman_xp -= 1
            else:
                self.build_xp -= 1

    def get_shaman_xp(self):
        self.shaman_xp += 1
        if random.randint(1, 100) <= self.parent.double_xp_chance:
            self.shaman_xp += 1
        if random.randint(1, 100) <= self.parent.xp_loss_chance:
            case = random.randint(1, 4)
            if case == 1:
                self.food_xp -= 1
            elif case == 2:
                self.gather_xp -= 1
            elif case == 3:
                self.fight_xp -= 1
            else:
                self.build_xp -= 1

    def get_build_xp(self):
        self.build_xp += 1
        if random.randint(1, 100) <= self.parent.double_xp_chance:
            self.build_xp += 1
        if random.randint(1, 100) <= self.parent.xp_loss_chance:
            case = random.randint(1, 4)
            if case == 1:
                self.food_xp -= 1
            elif case == 2:
                self.gather_xp -= 1
            elif case == 3:
                self.fight_xp -= 1
            else:
                self.shaman_xp -= 1

    def kill(self):
        self.parent.remove_pop(self)

    def work(self):
        if self.job = None:
            self.job = IdleJob(self)
        self.job.work()
