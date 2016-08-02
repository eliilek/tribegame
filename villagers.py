import pygame
import random
from pygame.locals import *

class XP(object):
    @property
    def xp(self):
        return self._xp
    @xp.setter
    def xp(self, x):
        self._xp = x
        if self._xp > self._xp_max:
            self._xp = self._xp_max
        elif self._xp < 0:
            self._xp = 0

    @property
    def level(self):
        return self._xp / self._xp_per_level

    def __init__(self, xp_per_level):
        self._xp = 2 * xp_per_level
        self._xp_max = 8 * xp_per_level - 1
        self._xp_per_level = xp_per_level

class Villager(object):
    @property
    def injury(self):
        return self._injury
    @injury.setter
    def injury(self, x):
        self._injury = x
        if self._injury > self.parent.injury_threshold:
            self.kill()
        elif self._injury < 0:
            self._injury = 0

    def __init__(self, parent, name, image):
        self.name = name
        self.image = pygame.image.load(image).convert()
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.xp = {"food":XP(parent.xp_per_level),"gather":XP(parent.xp_per_level),"fight":XP(parent.xp_per_level), "build":XP(parent.xp_per_level)}
        self._injury = 0
        self.job = None
        self.parent = parent

    def injure(self, val):
        self.injury += val

    def set_injury(self, val):
        self.injury = val

    def health_boxes(self):
        return self.injury - self.parent.injury_threshold

    def get_xp(self, key):
        if key == None:
            return None
        xp = 1
        if random.randint(1, 100) <= self.parent.double_xp_chance:  xp += 1
        try:
            self.xp[key].xp += xp
        except:
            self.xp[key] = XP(self.parent.xp_per_level)
            self.xp[key].xp += xp
        if random.randint(1, 100) <= self.parent.xp_loss_chance:
            up_for_loss = []
            for name, value in self.xp.items():
                if name != key: up_for_loss.append(value)
            random.choice(up_for_loss).xp -= 1

    def kill(self):
        self.parent.remove_pop(self)

    #Arg[0] is job to assign, Arg[1] is pass-through function
    def assign_job(self, args):
        self.job = args[0]
        if len(args) > 1:
            args[1]()

    def work(self):
        if self.job != None:
            self.job.work(self)
