import pygame
import jobs

def rand_name():
    return "Steve"

class TribeGame(object):
    def __init__(self, calendar, land, tribe_name, starting_pop, xp_per_level, size, starting_food = -1, starting_wood = 0, starting_stone = 0):
        self.tribe_name = tribe_name
        self.calendar = calendar
        self.calendar.begin()
        self.land = land
        self.event = None

        ###Change these to be the corner within the side menus
        self.land_x = 0
        self.land_y = 0

        self.xp_per_level = xp_per_level
        self.pop = []
        self._resources = {'wood':starting_wood, 'stone':starting_stone, 'food':(starting_food if starting_food != -1 else starting_pop * 6))}
        self.injury_threshold = 5
        self.healing_cap = 1
        self.surf = pygame.Surface(size)
        ###Render sidebar menus onto surf here
        for i in range(0, starting_pop):
            pop.append(Villager(self, rand_name()))

    def set_event(self, event):
        self.event = event

    def loop(self):
        self.land.loop()
        for menu in self.menus:
            menu.loop()

    def turn(self):
        for villager in pop:
            villager.work()
        event = self.calendar.next_turn()
        if event != None:
            event.run(self)

    def render(self):
        self.land.render(self.surf, self.land_x, self.land_y)
        if self.event != None:
            self.surf.blit(self.event.surface, (self.event.x_pos, self.event.y_pos))

    def remove_pop(self, child):
        self.pop.remove(child)

    def get_resource(self, key, num):
        if num > 0:
            try:
                if self._resources[key] > num:
                    self._resources[key] -= num
                    return num
                else:
                    val = self._resources[key]
                    self._resources[key] = 0
                    return val
            except:
                return 0
        else:
            try:
                self._resources[key] += num
            except:
                self._resources[key] = num

    def click(self, event):
        mpos = event.pos
        #Check which frame the click is in, pass to appropriate menu
        ###More logic here to check other menus###
        if self.event != None:
            if (type(self.event) == Menu.Alert) and self.event.is_my_click(mpos):
                self.event = None
            elif self.event.menu.is_my_click(mpos):
                self.event.menu.click(event)
        else:
            self.land.click((mpos[0] - self.land_x, mpos[1] - self.land_y))

    def key_down(self, key):
        self.land.key_down(key)

    def key_up(self, key):
        self.land.key_up(key)

    def enough_resources(self, required):
        try:
            for key, val in required:
                if self._resources[key] < val:
                    return False
            return True
        except:
            return False

    def available_villagers(self):
        free = []
        for villager in pop:
            if villager.job == None or isinstance(villager.job, jobs.IdleJob):
                free.append(villager)
        return free

if __name__ == "__main__":
    import GameEvent
    import villagers
    import tile
    import tilemanager

    cal = GameEvent.Calendar([None, None, None])
    tile1 = tile.Tile(None, "Forest", wood = 50)
    tile2 = tile.Tile(None, "Berries", food = 50)
    tile3 = tile.Tile(None, "Mountain", stone = 50)
    tile_man = tilemanager.TileManager(50, [tile1, tile2, tile3])
