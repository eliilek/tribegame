import pygame
import tribegame
import GameEvent
import Menu
from GameResources import *
import random

def load_for_tribegame():
    random_events = load_random_events()
    events = load_game_events(random_events)
    calendar = GameEvent.Calendar(events)

    return tribegame.TribeGame(calendar, land, tribe_name, starting_pop, xp_per_level, size)

def load_random_events():
    events = []
    #Random event 1
    title = "Injury Worsens"
    text = lambda villager:"Thing happened to " + villager.name + ". All are sad."
    requirements = lambda game_object:random.choice([villager for villager in game_object.pop if villager.injury > 0])
    options_text = ["Spare no expense in their treatment! (-5 food)", "Let the spirits heal him!", "This land is no place for the weak. Sharpen the knives."]
    options_funcs = {}
    options_funcs["Spare no expense in their treatment! (-5 food)"] = ()
    options_menu = Menu.StringMenu(MENU_BACKGROUND, options_text, options_funcs, MENU_FONT, MENU_FONT_SIZE, OPTIONS_COLOR, EVENT_WIDTH, EVENT_HEIGHT))
    events.append(GameEvent.GameEvent(title, text, options_menu, requirements))

def load_game_events():
    events = []
    #Event 1
