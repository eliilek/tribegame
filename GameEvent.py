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
        self.x_pos = (game_object.land_x + pygame.display.get_surface().get_width())/2 - event_surface.get_width()/2
        self.y_pos = (game_object.land_y + pygame.display.get_surface().get_height())/2 - event_surface.get_height()/2
        self.menu.set_position(((event_surface.get_width()/2 - self.menu.get_width()/2) + self.x_pos, event_surface.get_height() - (self.menu.get_height() + 5) + self.y_pos))
        game_object.event = self
        self.surface = event_surface
