import pygame
import copy
from jobs import WoodJob, FoodJob, StoneJob, HealJob

class Tile(object):
    def __init__(self, image, name, jobs = [], resources = {}, buildings = []):
        self.name = name
        self.buildings = buildings
        self.image = image
        self.jobs = jobs
        #Set it up with a surface displaying image
        self._resources = resources
        self.reachable = False

    def clone(self):
        return Tile(copy.copy(self.image), self.name, copy.deepcopy(self.jobs), copy.deepcopy(self.resources), copy.deepcopy(self.buildings))

    #Clone first
    def to_village(self, healing_cap):
        self.name = "Village"
        self.jobs.append(HealJob(self, healing_cap))

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
