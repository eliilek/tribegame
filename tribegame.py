import pygame

def rand_name():
    return "Steve"

class TribeGame():
    def __init__(self, calendar, land, tribe_name, starting_pop, xp_per_level, size, starting_wood = 0, starting_food = 0, starting_stone = 0):
        self.tribe_name = tribe_name
        self.calendar = calendar
        self.calendar.begin()
        self.land = land
        self.xp_per_level = xp_per_level
        self.pop = []
        self.wood = starting_wood
        self.stone = starting_stone
        self.ore = 0
        self.metal = 0
        self.injury_threshold = 5
        if starting_food == 0:
            self.food = self.starting_pop * 3
        else:
            self.food = self.starting_food
        self.surf = pygame.Surface(size)
        for i in range(0, starting_pop):
            pop.append(Villager(self, rand_name())

    def loop(self):
        for villager in pop:
            villager.loop()

    def turn(self):
        for villager in pop:
            villager.work()
        event = self.calendar.next_turn()
        if event != None:
            event.run(self)

    def render(self):
        pass

    def remove_pop(self, child):
        self.pop.remove(child)
