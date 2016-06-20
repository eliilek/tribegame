import pygame

class Tile(Object):
    @property
    def wood(self):
        return self._wood
    @wood.setter
    def wood(self, x):
        self._wood = x
        if self._wood < 0:
            self._wood = 0
        elif self._wood > self.wood_max:
            self._wood = self.wood_max

    @property
    def stone(self):
        return self._stone
    @stone.setter
    def stone(self, x):
        self._stone = x
        if self._stone < 0:
            self._stone = 0
        elif self._stone > self.stone_max:
            self._stone = self.stone_max

    @property
    def food(self):
        return self._food
    @food.setter
    def food(self, x):
        self._food = x
        if self._food < 0:
            self._food = 0
        elif self._food > self.food_max:
            self._food = self.food_max

    def __init__(self, image, jobs, name, wood = 0, stone = 0, food = 0, ore = 0):
        self.name = name
        self.buildings = []
        #Set it up with a surface displaying image
        self.jobs = jobs
        self._wood = self.wood_max = wood
        self._stone = self.stone_max = stone
        self._food = self.food_max = food
        self.ore = ore

    def harvest_wood(self, amount):
        if amount > self.wood:
            amount = self.wood
        self.wood -= amount
        return amount

    def harvest_stone(self, amount):
        if amount > self.stone:
            amount = self.stone
        self.stone -= amount
        return amount

    def harvest_food(self, amount):
        if amount > self.food:
            amount = self.food
        self.food -= amount
        return amount

    def harvest_ore(self, amount):
        if amount > self.ore:
            amount = self.ore
        self.ore -= amount
        return amount
