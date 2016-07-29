import random
from GameResources import *
import copy

class Job():
    def __init__(self, name, tile, injury_chance = 0, injury_severity = 1):
        self.tile = tile
        self.injury_chance = injury_chance
        self.injury_severity = injury_severity
        self.name = name
        self.working_villagers = []
        self.xp_type = None

    def work(self, villager):
        pass

class GatherJob(Job):
    def __init__(self, name, key, tile, xp_type, lower_bound, upper_bound, injury_chance = 0, injury_severity = 1):
        Job.__init__(self, name, tile, injury_chance, injury_severity)
        self.key = key
        self.xp_type = xp_type
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def work(self, villager):
        if isinstance(self.key, basestring):
            base_yield = random.randInt(self.lower_bound, self.upper_bound)
            if villager.xp[self.xp_type].level >= 2:
                attempt = base_yield * (villager.xp[self.xp_type].level * .20 + .60)
                injury_chance = self.injury_chance
            else:
                attempt = base_yield
                injury_chance = self.injury_chance + (5 * (2 - villager.xp[self.xp_type].level))
            gathered = self.tile.harvest(self.key, attempt)
            villager.parent.get_resource(self.key, -gathered)
            villager.get_xp(self.xp_type)
            if random.randint(1, 100) <= self.injury_chance:
                villager.injury += random.randint(1, self.injury_severity)
            villager.job = None
        else:
            for index, item in enumerate(self.key):
                gathered = tile.harvest(item, random.randInt(self.lower_bound[index], self.upper_bound))
                villager.parent.get_resource(item, -gathered)
            villager.get_xp(self.xp_type)
            if random.randint(1, 100) <= self.injury_chance:
                villager.injury += random.randint(1, self.injury_severity)
            villager.job = None

class HealJob(Job):
    def __init__(self, name, tile, healing_cap):
        Job.__init__(self, name, tile)
        self.healing_cap = healing_cap

    def work(self, villager):
        villager.injury -= random.randint(1, self.healing_cap)
        if villager.injury == 0:
            villager.job = None

class ConstructionJob(Job):
    def __init__(self, name, tile, building):
        Job.__init__(self, name, tile)
        self.xp_type = "build"
        if building.completion >= building.completion_progress:
            self.building = copy.deepcopy(building)
        else:
            self.building = building
        self.building.tile = tile
        self.building.completion = 0

    def work(self, villager):
        if self.building not in self.building.tile.buildings:
            self.building.tile.build(self.building)
        self.building.progress += 10
        if self.building.completion >= self.building.completion_progress:
            self.building.on_completion()
            villager.job = None
            self.tile.remove_job(self)
        villager.get_xp(self.xp_type)
        if random.randint(1, 100) <= self.injury_chance:
            villager.injury += random.randint(1, self.injury_severity)

class BuildingSelectJob(Job):
    def __init__(self, name, tile):
        Job.__init__(self, name, tile)

    def secondary_menu(self, tile_manager, tile, village):
        building_names = []
        building_funcs = {}
        for building in tile_manager.buildings:
            if tile.can_build(building):
                building_names.append(building.name)
                if (village.enough_resources(building.costs())):
                    building_funcs[building.name] = (tile_manager.jobs_to_villagers, ConstructionJob("Build " + building.name, self.tile, building))
                else:
                    building_funcs[building.name] = (lambda :None)
        new_menu = StringMenu(MENU_BACKGROUND, building_names, building_funcs, MENU_FONT, MENU_FONT_SIZE, MENU_FONT_COLOR, TILE_MENU_WIDTH, TILE_MENU_HEIGHT, TILE_MENU_BG, tile_manager.open_menu.x_pos, tile_manager.open_menu.y_pos)
        tile_manager.open_menu = new_menu
