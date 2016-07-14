import pygame

class Building(object):
    def __init__(self, name, image, completion_progress, jobs = [], unique = False):
        self.image = pygame.image.load(image).convert()
        self.name = name
        self.jobs = jobs
        self.tile = None
        self.progress = 0
        self.completion_progress = completion_progress
        self.unique = unique

    def requirements(self, tile):
        pass

    def costs(self):
        return {}

    def on_completion(self):
        pass

class Farm(Building):
    def __init__(self, name, image, completion_progress):
        Building.__init__(name, image, completion_progress)

    def requirements(self, tile):
        return tile.has_resource("food")

    def on_completion(self):
        self.tile.increase_regen("food", 3)

    def costs(self):
        return {"wood":20, "food": 10}
