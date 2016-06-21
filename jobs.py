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
    def __init__(self, tile, wood_min, wood_max, injury_chance = 0, injury_severity = 1):
        Job.__init__(self, tile, injury_chance, injury_severity)
        self.wood_min = wood_min
        self.wood_max = wood_max

    def work(self, villager):
        gathered_wood = tile.harvest_wood(random.randInt(self.wood_min, self.wood_max))
        villager.parent.wood += gathered_wood
        villager.get_gather_xp()
        if random.randint(1, 100) <= self.injury_chance:
            villager.injury += random.randint(1, self.injury_severity)

class FoodJob(Job):
    def __init__(self, tile, food_min, food_max, injury_chance = 0, injury_severity = 1):
        Job.__init__(self, tile, injury_chance, injury_severity)
        self.food_min = food_min
        self.food_max = food_max

    def work(self, villager):
        gathered_food = tile.harvest_food(random.randInt(self.food_min, self.food_max))
        villager.parent.food += gathered_food
        villager.get_food_xp()
        if random.randint(1, 100) <= self.injury_chance:
            villager.injury += random.randint(1, self.injury_severity)

class StoneJob(Job):
    def __init__(self, tile, stone_min, stone_max, injury_chance = 0, injury_severity = 1):
        Job.__init__(self, tile, injury_chance, injury_severity)
        self.stone_min = stone_min
        self.stone_max = stone_max

    def work(self, villager):
        gathered_stone = tile.harvest_stone(random.randInt(self.wood_min, self.wood_max))
        villager.parent.stone += gathered_stone
        villager.get_gather_xp()
        if random.randint(1, 100) <= self.injury_chance:
            villager.injury += random.randint(1, self.injury_severity)

class HealJob(Job):
    def __init__(self, tile, healing_cap):
        Job.__init__(self, tile)
        self.healing_cap = healing_cap

    def work(self, villager):
        villager.injury -= random.randint(1, self.healing_cap)
