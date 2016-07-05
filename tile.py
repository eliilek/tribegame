import pygame
import copy
from jobs import WoodJob, FoodJob, StoneJob, HealJob

class Building(object):
    def __init__(self, image, name, jobs = []):
        self.image = pygame.image.load(image).convert()
        self.name = name
        self.jobs = jobs

class Tile(object):
    def __init__(self, image, name, jobs = [], resources = {}, buildings = [], x = 0, y = 0):
        self.name = name
        self.buildings = buildings
        self.jobs = jobs
        self.image = pygame.image.load(image).convert()
        self._resources = resources
        self.reachable = False
        self.x = x
        self.y = y

    def clone(self, x = 0, y = 0):
        return Tile(copy.copy(self.image), self.name, copy.deepcopy(self.jobs), copy.deepcopy(self.resources), copy.deepcopy(self.buildings), x, y)

    #Clone first
    def to_village(self, healing_cap):
        self.name = "Village"
        self.jobs.append(HealJob(self, healing_cap))

    def build(self, building):
        ###Should remove the job to build this building
        self.buildings.append(building)
        for job in building.jobs:
            new_job = copy.deepcopy(job)
            new_job.tile = self
            self.jobs.append(new_job)

    def harvest(self, key, num):
        try:
            if self._resources[key][0] > num:
                self._resources[key][0] -= num
                return num
            else:
                val = self._resources[key][0]
                self._resources[key][0] = 0
                return val
        except:
            return 0

    def replenish(self):
        for key, tup in resources:
            if len(tup) == 2:
                tup[0] += 8
                if tup[0] > tup[1]: tup[0] = tup[1]
            elif len(tup) >= 3:
                tup[0] += tup[2]
                if tup[0] > tup[1]: tup[0] = tup[1]

    def available_jobs(self):
        if not self.reachable:
            ###MIGRATION JOB GOES HERE
            return None
        else:
            return self.jobs

    def render(self, screen, x, y):
        screen.blit(self.image, (x, y))
