import random

class Job():
    def __init__(self, tile, injury_chance = 0, injury_severity = 1):
        self.tile = tile
        self.injury_chance = injury_chance
        self.injury_severity = injury_severity

    def work(self):
        pass

class IdleJob(Job):
    pass

class WoodJob(Job):
    def __init__(self, tile, injury_chance = 0, injury_severity = 1, wood_min, wood_max):
        Job.__init__(self, tile, injury_chance, injury_severity)
        self.wood_min = wood_min
        self.wood_max = wood_max

    def work(self, villager):
        gathered_wood = tile.harvest_wood(random.randInt(self.wood_min, self.wood_max))
        villager.parent.wood += gathered_wood
        villager.get_gather_xp()
        if random.randint(1, 100) <= self.injury_chance:
            villager.injury += random.randint(1, self.injury_severity)

class HealJob(Job):
    def __init__(self, tile, healing_cap):
        Job.__init__(self, tile)
        self.healing_cap = healing_cap

    def work(self, villager):
        villager.injury -= random.randint(1, self.healing_cap)
