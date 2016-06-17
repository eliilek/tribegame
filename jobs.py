import random

class Job():
    def __init__(self, villager):
        self.villager = villager

    def work(self):
        pass

class IdleJob(Job):
    pass

class DangerousJob(Job):
    def __init__(self, villager, injury_chance, injury_severity):
        Job.__init__(self, villager)
        self.injury_chance = injury_chance
        self.injury_severity = injury_severity

class WoodJob(DangerousJob):
    def __init__(self, villager, injury_chance, injury_severity, wood_min, wood_max):
        DangerousJob.__init__(self, villager, injury_chance, injury_severity)
        self.wood_min = wood_min
        self.wood_max = wood_max

    def work(self):
        self.villager.parent.wood += random.randint(self.wood_min, self.wood_max)
        self.villager.get_gather_xp()
        if random.randint(1, 100) <= self.injury_chance:
            self.villager.injury += random.randint(1, self.injury_severity)

class HealJob(Job):
    def __init__(self, villager, healing_cap):
        Job.__init__(self, villager)
        self.healing_cap = healing_cap

    def work(self):
        self.villager.injury -= random.randint(1, self.healing_cap)
