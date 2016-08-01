import pygame
import jobs
import villagers
from GameResources import *
import Menu

def rand_name():
    return "Steve"

class TribeGame(object):
    def __init__(self, calendar, land, tribe_name, starting_pop, xp_per_level, size, starting_food = -1, starting_wood = 0, starting_stone = 0, parent = None):
        self.tribe_name = tribe_name
        self.calendar = calendar
        self.calendar.begin()
        self.land = land
        self.land.parent = self
        self.event = None
        self.parent = parent

        ###Change these to be the corner within the side menus
        self.land_rect = pygame.Rect(LAND_CORNERS)

        self.xp_per_level = xp_per_level
        self.double_xp_chance = 0
        self.xp_loss_chance = 5
        self.pop = []
        self._resources = {'wood':starting_wood, 'stone':starting_stone, 'food':(starting_food if starting_food != -1 else starting_pop * 6)}
        self.injury_threshold = 5
        self.healing_cap = 1
        self.surf = pygame.Surface(size)

        self.frame_objects = []
        next_turn = Menu.StringMenu("Resources/turn_button.jpg", ["Next Turn"], {"Next Turn": self.turn}, width = 150, height = 50, x_pos = SCREEN_SIZE[0] - 150, y_pos = SCREEN_SIZE[1] - 50)
        next_turn.mouse_over = lambda item: None
        next_turn.mouse_not_over = lambda item: None
        self.frame_objects.append(next_turn)


        for i in range(0, starting_pop):
            self.pop.append(villagers.Villager(self, rand_name(), "Resources/villager.jpg"))

    def set_event(self, event):
        self.event = event

    def set_alert(self, text, args = None):
        self.event = Menu.Alert(text, args)

    def loop(self):
        self.land.loop()

    def turn(self):
        for villager in self.pop:
            villager.work()
        event = self.calendar.next_turn()
        if event != None:
            event.run(self)
        if len(self.pop) == 0:
            self.game_over()

    def render(self, screen):
        for item in self.frame_objects:
            item.render(self.surf)
        self.land.render(self.surf, self.land_rect.x, self.land_rect.y)
        if self.event != None:
            self.event.render(self.surf)
        screen.blit(self.surf, (0, 0))

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
            print mpos, (mpos[0]-self.event.x_pos, mpos[1]-self.event.y_pos)
            if (type(self.event) == Menu.Alert) and self.event.is_my_click(mpos):
                self.event = None
                if len(self.pop) == 0:
                    parent._running = False
            elif self.event.menu.is_my_click(mpos):
                self.event.menu.click(event, (-self.event.x_pos, -self.event.y_pos))
        else:
            if self.land_rect.collidepoint(mpos):
                self.land.click((mpos[0] - self.land_rect.x, mpos[1] - self.land_rect.y))
            else:
                for item in self.frame_objects:
                    if item.is_my_click(mpos):
                        item.click(mpos)
                #Pass click to outer menus

    def key_down(self, key):
        self.land.key_down(key)

    def key_up(self, key):
        self.land.key_up(key)

    def enough_resources(self, required):
        try:
            for key in required:
                if self._resources[key] < required[key]:
                    return False
            return True
        except:
            return False

    def available_villagers(self):
        free = []
        for villager in self.pop:
            if villager.job == None:
                free.append(villager)
        return free

    def game_over(self):
        self.event = Menu.Alert("Your last villager has shuffled off this mortal coil. Years from now, another tribe may stumble across your \
            abandoned village and wonder what failure brought you to such ruin. But they will have no answer.")
