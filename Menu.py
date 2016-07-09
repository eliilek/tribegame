import pygame

class MenuItem(pygame.font.Font):
    def __init__(self, text, font = None, font_size = 30, font_color = (255, 255, 255), (pos_x, pos_y) = (0, 0), padding = 0, horizontal = False):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.to_blit = self.render(self.text, 1, self.font_color)
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
            pygame.transform.scale(background_screen, (self.width + 10, self.height + 10))
        x = (background_screen.get_width() / 2) - ((self.width if not horizontal else self.width - self.padding)/ 2)
        y = (background_screen.get_height() / 2) - ((self.height if horizontal else self.height - self.padding) / 2)
        self.to_blit = background_screen.blit(self.to_blit, (x, y))
        self.width = self.label.get_width()
        self.height = self.label.get_height()
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

class Menu():
    def __init__(self, image, funcs, width = pygame.display.get_surface().get_width(), height = pygame.display.get_surface().get_height(), x_pos = 0, y_pos = 0, horizontal):
        screen = pygame.image.load(image)
        self.screen = pygame.transform.scale(screen, (width, height))
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.funcs = funcs
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.horizontal = horizontal

        def render(self):
            for item in self.items:
                if item.is_mouse_over(pygame.mouse.get_pos()):
                    self.mouse_over(item)
                else:
                    self.mouse_not_over(item)
                self.screen.blit(item.to_blit, item.position)
            pygame.display.get_surface().blit(self.screen, (self.x_pos, self.y_pos))

        def click(self, event):
            pass

        def mouse_over(self, item):
            pass

        def mouse_not_over(self, item):
            pass

class StringMenu(Menu):
    #Items is a list of strings to be displayed
    #Funcs is a dictionary mapping strings to functions

    def __init__(self, image, items, funcs, font = None, font_size = 30, font_color = (255, 255, 255), width = pygame.display.get_surface().get_width(), height = pygame.display.get_surface().get_height(), button_bg = None, x_pos = 0, y_pos = 0, horizontal = False):
        Menu.__init__(self, image, funcs, width, height, x_pos, y_pos, horizontal)
        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item, padding = 10, horizontal)
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

    def is_my_click(self, mpos):
        pos_x = mpos[0]
        pos_y = mpos[1]
        if (pos_x >= self.x_pos and pos_x <= self.x_pos + self.screen_width) and (pos_y >= self.y_pos and pos_y <= self.y_pos + self.screen_height):
            return True
        return False

    def mouse_over(self, item):
        item.set_font_color((34, 255, 17))

    def mouse_not_over(self, item):
        item.set_font_color((255, 255, 255))

    def click(self, event):
        mpos = event.pos
        for item in self.items:
            if item.is_mouse_over(mpos):
                self.funcs[item.text]()

    def loop(self):
        pass

class ObjectMenu(Menu):
    #Items is a list of Objects with image attributes
    #Funcs is a dictionary mapping Objects to functions

    def __init__(self, image, items, funcs, width = pygame.display.get_surface().get_width(), height = pygame.display.get_surface().get_height(), x_pos = 0, y_pos = 0, horizontal = False):
        Menu.__init__(self, image, funcs, width, height, x_pos, y_pos, horizontal)
        self.items = []
        for index, item in enumerate(items):
