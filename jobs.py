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

class GatherJob(Job):
    def __init__(self, key, tile, lower_bound, upper_bound, injury_chance = 0, injury_severity = 1):
        Job.__init__(self, tile, injury_chance, injury_severity)
        self.key = key
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def work(self, villager):
        gathered = tile.harvest(self.key, random.randInt(self.lower_bound, self.upper_bound))
        villager.parent.get_resource(self.key, -gathered)
        villager.get_xp("gather")
        if random.randint(1, 100) <= self.injury_chance:
            villager.injury += random.randint(1, self.injury_severity)

class FoodJob(Job):
    def __init__(self, key, tile, lower_bound, upper_bound, injury_chance = 0, injury_severity = 1):
        Job.__init__(self, tile, injury_chance, injury_severity)
        self.key = key
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def work(self, villager):
        gathered = tile.harvest_food(self.key, random.randInt(self.lower_bound, self.upper_bound))
        villager.parent.get_resource(self.key, -gathered)
        villager.get_xp("food")
        if random.randint(1, 100) <= self.injury_chance:
            villager.injury += random.randint(1, self.injury_severity)

class HealJob(Job):
    def __init__(self, tile, healing_cap):
        Job.__init__(self, tile)
        self.healing_cap = healing_cap

    def work(self, villager):
        villager.injury -= random.randint(1, self.healing_cap)
