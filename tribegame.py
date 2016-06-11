import pygame

class TribeGame():
    def __init__(self, calendar, tribe_name, starting_pop, xp_per_level, size):
        self.tribe_name = tribe_name
        self.calendar = calendar
        self.turn = 0
        self.xp_per_level
        self.pop = []
        self.surf = pygame.Surface(size)
        for i in range(0, starting_pop):
            pop.append(Villager(rand_name(), self.xp_per_level))

    def loop():
        for villager in pop:
            villager.loop()

    def render():
        pass
