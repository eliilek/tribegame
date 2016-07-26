import pygame
import jobs

class Building(object):
    def __init__(self, name, image, completion_progress, jobs = [], unique = False):
        self.image = pygame.image.load(image).convert()
        self.name = name
        self.jobs = jobs
        self._tile = None
        self.progress = 0
        self.completion_progress = completion_progress
        self.unique = unique

    def requirements(self, tile):
        pass

    def costs(self):
        return {}

    def on_completion(self):
        pass
        
