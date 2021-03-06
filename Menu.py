import pygame
import TextWrapping
from GameResources import *

class Alert(pygame.font.Font):
    def __init__(self, text, args = None, background = MENU_BACKGROUND, font = MENU_FONT, font_size = MENU_FONT_SIZE, font_color = MENU_FONT_COLOR, (pos_x, pos_y) = ALERT_POSITION):
        pygame.font.Font.__init__(self, font, font_size)
        if not isinstance(text, basestring):
            text = text(args)
        text = TextWrapping.wrapline(text)
        labels = []
        for line in text:
            label = self.render(line, 1, font_color)
            labels.append(label)
        if isinstance(background, basestring):
            surface = pygame.image.load(background).convert()
        else:
            surface = background
        self.surface = pygame.transform.scale(surface, (labels[0].get_width() + 10, (labels[0].get_height() * len(labels)) + 10))
        for index, label in enumerate(labels):
            self.surface.blit(label, (5, 5 + (index * label.get_height()) + (index * 2)))
        self.x_pos = pos_x
        self.y_pos = pos_y

    def is_my_click(self, mpos):
        pos_x = mpos[0]
        pos_y = mpos[1]
        if (pos_x >= self.x_pos and pos_x <= self.x_pos + self.screen_width) and (pos_y >= self.y_pos and pos_y <= self.y_pos + self.screen_height):
            return True
        return False

    def render(self, surf):
        surf.blit(self.surface, (self.x_pos, self.y_pos))

class MenuItem(pygame.font.Font):
    def __init__(self, text, font = MENU_FONT, font_size = MENU_FONT_SIZE, font_color = MENU_FONT_COLOR, (pos_x, pos_y) = (0, 0), padding = 0, horizontal = False):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.background = None
        self.to_blit = self.label.copy()
        self.width = self.label.get_width()
        self.height = self.label.get_height()
        if horizontal:
            self.width += padding
        else:
            self.height += padding
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = (pos_x, pos_y)
        self.padding = padding

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def set_background(self, background_screen):
        if self.width > background_screen.get_width() or self.height > background_screen.get_height():
            self.background = pygame.transform.scale(background_screen, (self.width + 10, self.height + 10))
        else:
            self.background = background_screen
        x = (self.background.get_width() / 2) - ((self.label.get_width() if not horizontal else self.label.get_width() - self.padding)/ 2)
        y = (self.background.get_height() / 2) - ((self.label.get_height() if horizontal else self.label.get_height() - self.padding) / 2)
        self.to_blit = self.background.copy()
        self.to_blit.blit(self.label, (x, y))
        self.width = self.to_blit.get_width()
        self.height = self.to_blit.get_height()
        if horizontal:
            self.width += self.padding
        else:
            self.height += self.padding

    def is_mouse_over(self, (pos_x, pos_y)):
        if (pos_x >= self.pos_x and pos_x <= self.pos_x + self.width) and (pos_y >= self.pos_y and pos_y <= self.pos_y + self.height):
            return True
        return False

    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)
        self.to_blit = self.label.copy()

class Menu():
    #image is the path

    def __init__(self, image, funcs, width = None, height = None, x_pos = 0, y_pos = 0, horizontal = False):
        if width == None:
            width = pygame.display.get_surface().get_width()
        if height == None:
            height = pygame.display.get_surface().get_height()
        if isinstance(image, basestring):
            screen = pygame.image.load(image)
        else:
            screen = image
        self.screen = pygame.transform.scale(screen, (width, height))
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.funcs = funcs
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.horizontal = horizontal

    def render(self, screen, offset = (0, 0)):
        for item in self.items:
            mpos = pygame.mouse.get_pos()
            if item.is_mouse_over((mpos[0] - self.x_pos + offset[0], mpos[1] - self.y_pos + offset[1])):
                self.mouse_over(item)
            else:
                self.mouse_not_over(item)
            self.screen.blit(item.to_blit, item.position)
        screen.blit(self.screen, (self.x_pos, self.y_pos))

    def click(self, mpos, offset = (0, 0)):
        try:
            mpos = mpos.pos
        except:
            pass
        for item in self.items:
            if item.is_mouse_over((mpos[0] - self.x_pos + offset[0], mpos[1] - self.y_pos + offset[1])):
                try:
                    if len(self.funcs[item.text]) == 1:
                        self.funcs[item.text][0]()
                    else:
                        self.funcs[item.text][0](self.funcs[item.text][1:])
                except TypeError:
                    self.funcs[item.text]()

    def mouse_over(self, item):
        pass

    def mouse_not_over(self, item):
        pass

    def is_my_click(self, mpos):
        pos_x = mpos[0]
        pos_y = mpos[1]
        if (pos_x >= self.x_pos and pos_x <= self.x_pos + self.screen_width) and (pos_y >= self.y_pos and pos_y <= self.y_pos + self.screen_height):
            return True
        return False

class StringMenu(Menu):
    #Items is a list of strings to be displayed
    #Funcs is a dictionary mapping strings to tuples of format (function, arg, arg, arg)
    #Funcs requiring args must unpack args from tuple

    def __init__(self, image, items, funcs, font = None, font_size = 30, font_color = (255, 255, 255), width = None, height = None, button_bg = None, x_pos = 0, y_pos = 0, horizontal = False, item_padding = 10, title = None):
        if width == None:
            width = pygame.display.get_surface().get_width()
        if height == None:
            height = pygame.display.get_surface().get_height()
        Menu.__init__(self, image, funcs, width, height, x_pos, y_pos, horizontal)
        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item, padding = item_padding, horizontal = horizontal, font_size = font_size)
            if button_bg:
                menu_item.set_background(pygame.image.load(button_bg))
            if self.horizontal:
                t_w = len(items) * menu_item.width
                pos_x = (self.screen_width / 2) - (t_w / 2) + ((index * 2) + index * menu_item.width)
                pos_y = (self.screen_height / 2) - (menu_item.height / 2)
            else:
                t_h = len(items) * menu_item.height
                pos_x = (self.screen_width / 2) - (menu_item.width / 2)
                pos_y = (self.screen_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

    def mouse_over(self, item):
        item.set_font_color(MENU_HIGHLIGHT_COLOR)

    def mouse_not_over(self, item):
        item.set_font_color(MENU_FONT_COLOR)

    def loop(self):
        pass

class TopBarMenu(StringMenu):
    def __init__(self, image, game_object, font = None, font_size = 20, font_color = (255, 255, 255), width = None, height = None):
        self.game_object = game_object
        self.prev_resources = [key + ": " + str(self.game_object._resources[key]) for key in self.game_object._resources]
        self.width = width
        self.height = height
        StringMenu.__init__(self, image, self.prev_resources, {item: lambda:None for item in self.prev_resources}, font, font_size, font_color, self.width, self.height, horizontal = True)

    def mouse_over(self, item):
        pass

    def mouse_not_over(self, item):
        pass

    def loop(self):
        if self.prev_resources != [key + ": " + str(self.game_object._resources[key]) for key in self.game_object._resources]:
            StringMenu.__init__(self, image, resources, {item: lambda:None for item in items}, None, 20, (255, 255, 255), self.width, self.height, horizontal = True)

#Villager image on left, right is villager name, relevant villager XP beneath, centered on villager image height
class VillagerMenuItem():
    def __init__(self, villager, relevant_xp, (pos_x, pos_y) = (0, 0), padding = 5):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = (pos_x, pos_y)
        self.background = None
        self.villager = villager
        self.padding = padding
        self.relevant_xp = relevant_xp
        temp_font = pygame.font.Font(None, VILLAGER_MENU_FONT_SIZE)
        name_label = temp_font.render(villager.name, 1, MENU_FONT_COLOR)
        try:
            xp_label = temp_font.render(villager.xp[self.relevant_xp].level, 1, MENU_FONT_COLOR)
        except:
            xp_label = temp_font.render("No relevant XP", 1, MENU_FONT_COLOR)
        self.base = pygame.Surface((villager.image.get_width() + padding + max(name_label.get_width(), xp_label.get_width()), villager.image.get_height()))
        self.width = self.base.get_width()
        self.height = self.base.get_height()
        self.base.blit(villager.image, (0,0))
        self.base.blit(name_label, (((self.width + villager.image.get_width() + padding)/2) - (name_label.get_width()/2), (self.height/3) - name_label.get_height()/2))
        self.base.blit(xp_label, (((self.width + villager.image.get_width() + padding)/2) - (xp_label.get_width()/2), (self.height * 2 / 3) - xp_label.get_height()/2))
        self.to_blit = self.base.copy()

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def set_background(self, background_screen):
        if self.width > background_screen.get_width() or self.height > background_screen.get_height():
            self.background = pygame.transform.scale(background_screen, (self.width + 10, self.height + 10))
        else:
            self.background = background_screen
        x = (self.background.get_width() / 2) - (self.base.get_width() / 2)
        y = (self.background.get_height() / 2) - (self.base.get_height() / 2)
        self.to_blit = self.background.copy()
        self.to_blit.blit(self.base, (x, y))
        self.width = self.to_blit.get_width()
        self.height = self.to_blit.get_height()

    def is_mouse_over(self, (pos_x, pos_y)):
        if (pos_x >= self.pos_x and pos_x <= self.pos_x + self.width) and (pos_y >= self.pos_y and pos_y <= self.pos_y + self.height):
            return True
        return False

    def set_font_color(self, rgb_tuple):
        temp_font = pygame.font.Font(None, VILLAGER_MENU_FONT_SIZE)
        name_label = temp_font.render(self.villager.name, 1, rgb_tuple)
        try:
            xp_label = temp_font.render(self.villager.xp[self.relevant_xp].level, 1, rgb_tuple)
        except:
            xp_label = temp_font.render("No relevant XP", 1, rgb_tuple)
        self.base = pygame.Surface(((self.villager.image.get_width() + self.padding + max(name_label.get_width(), xp_label.get_width()), self.villager.image.get_height())))
        self.base.blit(self.villager.image, (0,0))
        self.base.blit(name_label, (((self.width + self.villager.image.get_width() + self.padding)/2) - (name_label.get_width()/2), (self.height/3) - name_label.get_height()/2))
        self.base.blit(xp_label, (((self.width + self.villager.image.get_width() + self.padding)/2) - (xp_label.get_width()/2), (self.height * 2 / 3) - xp_label.get_height()/2))
        if self.background != None:
            x = (self.background.get_width() / 2) - (self.base.get_width() / 2)
            y = (self.background.get_height() / 2) - (self.base.get_height() / 2)
            self.to_blit = self.background.copy()
            self.to_blit.blit(self.base, (x, y))
        else:
            self.to_blit = self.base.copy()

class VillagerJobMenu(Menu):
    def __init__(self, image, villagers, funcs, relevant_xp, width = None, height = None, button_bg = None, x_pos = 0, y_pos = 0, horizontal = False):
        if width == None:
            width = pygame.display.get_surface().get_width()
        if height == None:
            height = pygame.display.get_surface().get_height()
        Menu.__init__(self, image, funcs, width, height, x_pos, y_pos, horizontal)
        self.items = []
        for index, villager in enumerate(villagers):
            menu_item = VillagerMenuItem(villager, relevant_xp)
            if button_bg != None:
                menu_item.set_background(pygame.image.load(button_bg))
            if self.horizontal:
                t_w = len(villagers) * menu_item.width
                pos_x = (self.screen_width / 2) - (t_w / 2) + ((index * 2) + index * menu_item.width)
                pos_y = (self.screen_height / 2) - (menu_item.height / 2)
            else:
                t_h = len(villagers) * menu_item.height
                pos_x = (self.screen_width / 2) - (menu_item.width / 2)
                pos_y = (self.screen_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

    def mouse_over(self, item):
        item.set_font_color(MENU_HIGHLIGHT_COLOR)

    def mouse_not_over(self, item):
        item.set_font_color(MENU_FONT_COLOR)

    def loop(self):
        #Animate villager images if animated
        pass

    def click(self, mpos, offset):
        try:
            mpos = mpos.pos
        except:
            pass
        for item in self.items:
            if item.is_mouse_over((mpos[0] - self.x_pos + offset[0], mpos[1] - self.y_pos + offset[1])):
                if len(self.funcs[item.villager]) == 1:
                    self.funcs[item.villager][0]()
                else:
                    self.funcs[item.villager][0](self.funcs[item.villager][1:])
