import pygame
from GameResources import *
import TextWrapping

class Calendar:
    def __init__(self, events):
        self.events = events

    def begin(self):
        self.turn=0

    def next_turn(self):
        self.turn += 1
        return self.events[self.turn-1]

    def get_length(self):
        return len(self.events)

class GameEvent:
    def __init__(self, title, text, options_menu):
        self.title = title
        self.text = text
        self.menu = options_menu
        self.font = pygame.font.Font(MENU_FONT, MENU_FONT_SIZE)

    def run(self, game_object):
        lines = TextWrapping.wrapline(text, self.font, EVENT_WIDTH - 10)
        event_surface = pygame.image.load(EVENT_BACKGROUND).convert()
        event_surface = pygame.transform.scale(event_surface, (EVENT_WIDTH, EVENT_HEIGHT))
        #position on main screen
        x_pos = (game_object.land_x + pygame.display.get_surface().get_width())/2 - event_surface.get_width()/2
        y_pos = (game_object.land_y + pygame.display.get_surface().get_height())/2 - event_surface.get_height()/2
