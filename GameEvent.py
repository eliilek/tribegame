import pygame
from GameResources import *
import TextWrapping
import random

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

class RandomEvent:
    def __init__(self, random_event_list):
        self.random_event_list = random_event_list

    def run(game_object):
        checked_events = []
        while(len(self.random_event_list) > 0):
            event = self.random_event_list.remove(random.choice(self.random_event_list))
            checked_events.append(event)
            if event.requirements_met(game_object):
                self.random_event_list += checked_events
                event.run(game_object)
                break
        else:
            self.random_event_list = checked_events
            ###Run none event, nothing much happened?

class GameEvent:
    def __init__(self, title, text, options_menu, requirements_func = lambda game_object:True):
        self.title = title
        self.text = text
        self.menu = options_menu
        self.font = pygame.font.Font(MENU_FONT, MENU_FONT_SIZE)
        self.requirements_met = requirements_func

    #If text/title is not a string, it's a function that takes the return type of requirements_met
    def run(self, game_object):
        args = self.requirements_met(game_object)
        for key in self.menu.funcs:
            self.menu.funcs[key] += [game_object, args]
        if not instanceof(self.title, basestring):
            self.title = self.title(args)
        if not instanceof(self.text, basestring):
            self.text = self.text(args)
        lines = TextWrapping.wrapline(self.text, self.font, EVENT_WIDTH - 10)
        rendered_lines = [self.font.render(self.title, 1, MENU_FONT_COLOR)]
        line_height = rendered_lines.get_height()
        text_surface = pygame.Surface(EVENT_WIDTH - 10, line_height * (len(lines) + 2))
        text_surface.blit(rendered_lines[0], (text_surface.get_width()/2 - rendered_lines[0].get_width()/2, 0))
        for index, line in enumerate(lines):
            rendered_lines.append(self.font.render(line, 1, MENU_FONT_COLOR))
            text_surface.blit(rendered_lines[index + 1], (0, (line_height * (index + 2)) + 2 * index))
        event_surface = pygame.image.load(EVENT_BACKGROUND).convert()
        event_surface = pygame.transform.scale(event_surface, (EVENT_WIDTH, max(EVENT_HEIGHT, text_surface.get_height() + EVENT_MIN_PADDING + self.menu.get_height())))
        event_surface.blit(text_surface, (5, 5))
        event_surface.blit(self.menu, (event_surface.get_width()/2 - self.menu.get_width()/2, event_surface.get_height() - (self.menu.get_height() + 5)))
        #position on main screen
        self.x_pos = (game_object.land_rect.x + pygame.display.get_surface().get_width())/2 - event_surface.get_width()/2
        self.y_pos = (game_object.land_rect.y + pygame.display.get_surface().get_height())/2 - event_surface.get_height()/2
        self.menu.set_position(((event_surface.get_width()/2 - self.menu.get_width()/2) + self.x_pos, event_surface.get_height() - (self.menu.get_height() + 5) + self.y_pos))
        game_object.event = self
        self.surface = event_surface
