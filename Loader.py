import pygame
import tribegame
import GameEvent
import Menu
from GameResources import *
import random

def multi_function(args):
    for i in range(len(args)/2):
        args[i * 2](args[(i * 2) + 1])

def load_for_tribegame():
    random_events = load_random_events()
    events = load_game_events(random_events)
    calendar = GameEvent.Calendar(events)

    return tribegame.TribeGame(calendar, land, tribe_name, starting_pop, xp_per_level, size)

def load_random_events():
    events = []
    #Random event 1
    title = "Injury Goes Bad"
    text = lambda villager:"""Bad things happen. Sometimes bad things happen, and then just keep happening. This is one of those times.
        Rather than healing, """ + villager.name + """'s injury has started to smell foul and turn all sorts of wrong colors."""
    requirements = lambda game_object:(random.choice([villager for villager in game_object.pop if villager.injury > 0]) \
        if len([villager for villager in game_object.pop if villager.injury > 0]) > 0 else False)
    options_text = ["A little rest and a good meal is all they need. They'll be fine. (-5 food)", \
        "Cut away the rot! We must do everything in our power to save their life! (+1 injury)", \
        "Only the spirits can decide their fate now.", "This land is no place for the weak. Sharpen the knives."]
    options_funcs = {}
    success_text = lambda villager: "After a long night fighting pain and injury, " + villager.name + " emerged victorious!"
    failure_text = lambda villager: "The gods are cruel and capricious. " + villager.name + " has departed for what lies beyond."
    options_funcs["A little rest and a good meal is all they need. They'll be fine. (-5 food)"] = [lambda game_object,villager: \
        ((game_object.get_resource("food", 5) and (game_object.set_event(Alert(success_text, villager)) \
        if random.random() < .6 else villager.set_injury(game_object.injury_threshold + 1) and game_object.set_event(Alert(failure_text, villager)))) \
        if game_object.enough_resources({"food": 5}) else None)]
    options_funcs["Cut away the rot! We must do everything in our power to save their life! (+1 injury)"] = [lambda game_object,villager: \
        ((villager.set_injury(villager.injury + 1) if random.random() < .9 else \
        villager.set_injury(game_object.injury_threshold + 1) and game_object.set_event(Alert(failure_text, villager)))] \
        if villager.injury < game_object.injury_threshold else None)
    options_funcs["Only the spirits can decide their fate now."] = [lambda game_object,villager: \
        (game_object.set_event(Alert(success_text, villager)) \
        if random.random() < .3 else villager.set_injury(game_object.injury_threshold + 1) and game_object.set_event(Alert(failure_text, villager)))]
    options_funcs["This land is no place for the weak. Sharpen the knives."] = [lambda game_object,villager: \
        villager.set_injury(game_object.injury_threshold + 1) and game_object.set_event(Alert(failure_text, villager))]
    options_menu = Menu.StringMenu(MENU_BACKGROUND, options_text, options_funcs, MENU_FONT, MENU_FONT_SIZE, OPTIONS_COLOR, EVENT_WIDTH, EVENT_HEIGHT))
    events.append(GameEvent.GameEvent(title, text, options_menu, requirements))

def load_game_events():
    events = []
    #Event 1
