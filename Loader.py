import pygame
from tribegame import TribeGame
import GameEvent
import Menu
from Menu import Alert
from GameResources import *
import random
import tilemanager
import tile
import jobs
import Building
from villagers import Villager

#Takes 2 lists of lists and a selector function
#The first item in each list is the function to call, the rest are arguments to be passed to that function
#Arguments will be passed as a list, need to be unpacked
#Selector returns true for success, false for failure
def multi_function_lambda(args):
    success = args[0]
    failure = args[1]
    selector = args[2]
    if len(args) == 6:
        needed_condtion = args[3]
        game_object = args[4]
        requirements = args[5]
    else:
        needed_condition = None
        game_object = args[3]
        requirements = args[4]

    if needed_condition != None:
        if (len(needed_condition) == 1) and (needed_condition[0]() == False):
            return None
        elif len(needed_condition) > 1:
            for i in range(1, len(needed_condition[1:]) + 1):
                if needed_condition[i] == "game_object":
                    needed_condition[i] = game_object
                elif needed_condition[i] == "requirements":
                    needed_condition[i] = requirements
            if needed_condition[0](needed_condition[1:]) == False:
                return None
    if selector():
        to_perform = success
    else:
        to_perform = failure
    for func in to_perform:
        if len(func) == 1:
            func[0]()
        else:
            for i in range(1, len(func[1:]) + 1):
                if func[i] == "game_object":
                    func[i] = game_object
                elif func[i] == "requirements":
                    func[i] = requirements
            func[0](func[1:])

def load_for_tribegame():
    images = load_images()
    random_events = load_random_events(images)
    events = load_game_events(random_events, GAME_LENGTH, images)
    calendar = GameEvent.Calendar(events)

    progenitor_tiles = load_tiles()

    #progenitor_buildings = load_buildings()
    progenitor_buildings = []
    land = tilemanager.TileManager(LAND_SIZE, progenitor_tiles, progenitor_buildings, LAND_CORNERS[1][0], LAND_CORNERS[1][1], images = images)

    tribe_name = "The Demo Tribe"

    starting_pop = 6

    xp_per_level = 3

    size = SCREEN_SIZE

    return TribeGame(calendar, land, tribe_name, starting_pop, xp_per_level, size, images = images)

def load_tiles():
    #Plains Tile
    plains = tile.Tile("Resources/plains.jpg", "Plains", [jobs.GatherJob("Forage", "food", None, "food", 3, 3), \
jobs.GatherJob("Hunt Small Game", ("food", "hides"), None, "food", (4, 1), (5, 2), 5, 1)], resources ={"food":(50, 50, 5), "hides":(20, 20, 0)})
    progenitor_tiles.append(plains)
    forest = tile.Tile("Resources/forest.jpg", "Forest", [jobs.GatherJob("Gather Wood", "wood", None, "gather", 10, 10)], resources = {"wood":(250, 250, 8)})
    progenitor_tiles.append(forest)
    rocks = tile.Tile("Resources/rocky.jpg", "Rocky Outcrop", [jobs.GatherJob("Gather Stone", "stone", None, "gather", 4, 4)], resources = {"stone":(200, 200, 0)})
    progenitor_tiles.append(rocks)

def load_images():
    images = {}
    images["village"] = pygame.image.load("Resources/village.jpg").convert()
    images["village"].set_colorkey((255, 255, 255))
    images["menu_background"] = pygame.image.load("Resources/menu.jpg").convert()

    return images

def load_buildings():
    buildings = []
    #Farm Building
    farm = Building.Building("Farm", "Resources/farm.png", 40)
    farm.requirements = lambda tile:tile.has_resource("food")
    farm.costs = lambda :{"wood":20, "food": 10}
    farm.on_completion = lambda :self.tile.increase_regen("food", 3)
    farm.progress = farm.completion_progress
    buildings.append(farm)
    #Quary Building
    quarry = Building.Building("Quarry", "Resources/quarry.png", 40)
    quarry.requirements = lambda tile:tile.has_resource("stone")
    quarry.costs = lambda :{"wood":20, "stone": 10}
    quarry.on_completion = lambda :self.tile.increase_multiplier("stone", 0.1)
    quarry.progress = quarry.completion_progress
    buildings.append(quarry)

def load_random_events(images):
    events = []
    try:
        menu_background = images["menu_background"]
    except:
        menu_background = MENU_BACKGROUND

    #Random event 1
    title = "Injury Goes Bad"
    text = lambda villager:"Bad things happen. Sometimes bad things happen, and then just keep happening. This is one of those times. \
Rather than healing, " + villager.name + "'s injury has started to smell foul and turn all sorts of wrong colors."
    requirements = lambda game_object:(random.choice([villager for villager in game_object.pop if villager.injury > 0]) \
if len([villager for villager in game_object.pop if villager.injury > 0]) > 0 else False)
    options_text = ["A little rest and a good meal is all they need. They'll be fine. (-5 food)", \
"Cut away the rot! We must do everything in our power to save their life! (+1 injury)", \
"Only the spirits can decide their fate now.", "This land is no place for the weak. Sharpen the knives."]
    options_funcs = {}
    success_text = lambda villager: "After a long night fighting pain and injury, " + villager.name + " emerged alive! For now..."
    failure_text = lambda villager: "The gods are cruel and capricious. " + villager.name + " has departed for what lies beyond."
    murder_text = lambda villager: "This land is harsh. " + villager.name + "'s sacrifice strengthens the tribe."
    options_funcs["A little rest and a good meal is all they need. They'll be fine. (-5 food)"] = [multi_function_lambda, \
[[TribeGame.get_resource, "game_object", "food", 5], [TribeGame.set_alert, "game_object", success_text, "requirements"]], \
[[TribeGame.get_resource, "game_object", "food", 5], [Villager.set_injury, "requirements", 1023], [TribeGame.set_alert, "game_object", failure_text, "requirements"]], \
(lambda :random.random() < .6), [TribeGame.enough_resources, "game_object", {"food":5}]]
    options_funcs["Cut away the rot! We must do everything in our power to save their life! (+1 injury)"] = [multi_function_lambda, \
[[Villager.injure, "requirements", 1], [TribeGame.set_alert, "game_object", success_text, "requirements"]], \
[[Villager.set_injury, "requirements", 1023], [TribeGame.set_alert, "game_object", failure_text, "requirements"]], \
(lambda: random.random() < .9), [Villager.health_boxes, "requirements"]]
    options_funcs["Only the spirits can decide their fate now."] = [multi_function_lambda, [[TribeGame.set_alert, "game_object", success_text, "requirements"]], \
[[Villager.set_injury, "requirements", 1023], [TribeGame.set_alert, "game_object", failure_text, "requirements"]], (lambda: random.random() < .3)]
    options_funcs["This land is no place for the weak. Sharpen the knives."] = [multi_function_lambda, \
[[Villager.set_injury, "requirements", 1023], [TribeGame.set_alert, "game_object", murder_text, "requirements"]], [], lambda: True]
    options_menu = Menu.StringMenu(menu_background, options_text, options_funcs, MENU_FONT, MENU_FONT_SIZE, OPTIONS_COLOR, EVENT_WIDTH, EVENT_HEIGHT)
    events.append(GameEvent.GameEvent(title, text, options_menu, requirements))

    #Random event 2
    title = "Wild Beasts"
    text = "Everything has to eat. Some things like to eat other people's food. During the night the villagers hear scratching and shuffling noises \
coming from the food storage."
    requirements = lambda game_object:(random.choice(game_object.pop) if game_object.enough_resources({"food":5}) else False)
    options_text = ["Better they eat our dinner than our bodies. Stay safe indoors.", "Nothing in this land is scarier than we are! Frighten them off!", \
"How nice of our food to come to us! Ready the spears!"]
    options_funcs = {}
    frighten_success = "The beasts took one look at us and ran off!"
    frighten_failure = lambda villager:"Something in this land is scarier than we are. They attacked, and " + villager.name + " was injured in the struggle."
    attack_success = "Moving quickly and efficiently, the warriors dispatch the beasts. They shall make a fine feast! (+7 food)"
    attack_failure = lambda villager:"You should always respect even the lowest of enemies. " + villager.name + " forgot this, and paid in blood. (+4 food)"

    options_funcs["Better they eat our dinner than our bodies. Stay safe indoors."] = [multi_function_lambda, [[TribeGame.get_resource, "game_object", "food", 5], \
[TribeGame.set_alert, "game_object", "When the sun rises, your villagers are all whole and healthy, though hungrier than before. (-5 food)"]], [], (lambda: True)]
    options_funcs["Nothing in this land is scarier than we are! Frighten them off!"] = [multi_function_lambda, \
[[TribeGame.set_alert, "game_object", frighten_success]], [[Villager.injure, "requirements", 2], [TribeGame.set_alert, "game_object", frighten_failure, "requirements"]], \
(lambda :random.random() < .8)]
    options_funcs["How nice of our food to come to us! Ready the spears!"] = [multi_function_lambda, [[TribeGame.get_resource, "game_object", "food", -7], \
[TribeGame.set_alert, "game_object", attack_success]], [[TribeGame.get_resource, "game_object", "food", -4], [Villager.injure, "requirements", 2], \
[TribeGame.set_alert, "game_object", attack_failure, "requirements"]], (lambda: random.random < .4)]
    options_menu = Menu.StringMenu(menu_background, options_text, options_funcs, MENU_FONT, VILLAGER_MENU_FONT_SIZE, OPTIONS_COLOR, EVENT_WIDTH, EVENT_HEIGHT)
    events.append(GameEvent.GameEvent(title, text, options_menu, requirements))

    return events

def load_game_events(random_events, length, images):
    events = [None for i in range(length)]
    #Scheduled events

    #Random events
    random_event = GameEvent.RandomEvent(random_events)
    for index, event in enumerate(events):
        if event == None:
            events[index] = random_event
    return events
