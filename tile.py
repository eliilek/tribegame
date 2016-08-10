import pygame
import copy
from GameResources import *
import jobs

class Tile(object):
    def __init__(self, image, name, tile_jobs = [], resources = {}, buildings = [], x = 0, y = 0):
        self.name = name
        self.base_name = name
        self.buildings = buildings
        self.tile_jobs = tile_jobs
        if isinstance(image, basestring):
            self.image = pygame.image.load(image).convert()
            self.image = pygame.transform.scale(self.image, TILE_SIZE)
        else:
            self.image = image
        self.renderable = self.image.copy()
        self._resources = resources
        self.reachable = False
        self.x = x
        self.y = y

    def clone(self, x = 0, y = 0):
        new_tile = Tile(copy.copy(self.image), self.name, copy.deepcopy(self.tile_jobs), copy.deepcopy(self._resources), copy.deepcopy(self.buildings), x, y)
        for job in new_tile.tile_jobs:
            job.tile = new_tile
        return new_tile

    def can_build(self, building):
        if building.unique and (building.name in (building.name for building in buildings)):
            return False
        return building.requirements(tile)

    def has_resource(self, key):
        try:
            self._resources[key]
            return True
        except:
            return False

    def increase_multiplier(self, key, val):
        try:
            if len(self._resources[key]) >= 4:
                self._resources[key][3] += val
            elif len(self._resources[key]) >= 3:
                self._resources[key] += (1 + val, )
            else:
                self._resources[key] += (0, 1 + val)
        except:
            pass

    def increase_regen(self, key, val):
        try:
            if len(self._resources[key]) >= 3:
                self._resources[key][2] += val
            else:
                self._resources[key] += (val, )
        except:
            pass

    #Clone first
    def to_village(self, healing_cap, village_image):
        self.name = "Village"
        self.tile_jobs.append(jobs.HealJob("Rest", self, healing_cap))
        if isinstance(village_image, basestring):
            village_image = pygame.image.load(village_image)
        village_image = pygame.transform.scale(village_image, (40, 40))
        self.renderable.blit(village_image, (15, 15))
        ###Add procreation job

    def to_base(self):
        self.name = self.base_name
        for job in self.tile_jobs:
            if isinstance(job, jobs.HealJob):
                self.tile_jobs.remove(job)
        self.renderable = self.image.copy()

    def build(self, building):
        self.buildings.append(building)
        self.tile_jobs.append(building.construction_job)

    def harvest(self, key, num):
        try:
            if self._resources[key][0] > num:
                self._resources[key][0] -= num
                if len(self._resources[key]) >= 4:
                    num *= self._resources[key][3]
                return int(num + 0.5)
            else:
                val = self._resources[key][0]
                self._resources[key][0] = 0
                if len(self._resources[key]) >= 4:
                    val *= self._resources[key][3]
                return int(val + 0.5)
        except:
            return 0

    def replenish(self):
        for key, tup in resources:
            if len(tup) >= 3:
                tup[0] += tup[2]
                if tup[0] > tup[1]: tup[0] = tup[1]

    def available_jobs(self):
        if not self.reachable:
            ###MIGRATION JOB GOES HERE
            return []
        else:
            return self.tile_jobs

    def remove_job(self, job):
        if job in self.tile_jobs:
            self.tile_jobs.remove(job)

    def render(self, screen, x, y):
        screen.blit(self.renderable, (x, y))
