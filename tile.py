import pygame
import copy

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
    def to_village(self, healing_cap):
        self.name = "Village"
        self.jobs.append(HealJob(self, healing_cap))
        ###Add procreation job

    def build(self, building):
        self.buildings.append(building)
        self.jobs.append(building.construction_job)

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
                return val
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
            return None
        else:
            return self.jobs

    def remove_job(self, job):
        if job in self.jobs:
            self.jobs.remove(job)

    def render(self, screen, x, y):
        screen.blit(self.image, (x, y))
