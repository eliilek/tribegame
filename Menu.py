import pygame

class MenuItem(pygame.font.Font):
    def __init__(self, text, font = None, font_size = 30, font_color = (255, 255, 255), (pos_x, pos_y) = (0, 0), padding = 0):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_width()
        self.height = self.label.get_height() + padding
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = (pos_x, pos_y)

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def set_background(self, background_screen):
        if self.width > background_screen.get_width() or self.height > background_screen.get_height():
            pygame.transform.scale(background_screen, (self.width + 10, self.height + 10))
        x = (background_screen.get_width() / 2) - (self.width / 2)
        y = (background_screen.get_height() / 2) - ((self.height - padding) / 2)
        self.label = background_screen.blit(self.label, (x, y))
        self.width = self.label.get_width()
        self.height = self.label.get_height() + padding

    def is_mouse_over(self, (pos_x, pos_y)):
        if (pos_x >= self.pos_x and pos_x <= self.pos_x + self.width) and (pos_y >= self.pos_y and pos_y <= self.pos_y + self.height):
            return True
        return False

    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)

class StringMenu():
    #Items is a list of strings to be displayed
    #Funcs is a dictionary mapping strings to functions
    def __init__(self, image, items, funcs, font = None, font_size = 30, font_color = (255, 255, 255), width = pygame.display.get_surface().get_width(), height = pygame.display.get_surface().get_height(), button_bg = None):
        screen = pygame.image.load(image)
        self.screen = pygame.transform.scale(screen, (width, height))
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.items = []
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self.funcs = funcs
        for index, item in enumerate(items):
            menu_item = MenuItem(item, padding = 10)
            if button_bg:
                menu_item.set_background(pygame.image.load(button_bg))
            t_h = len(items) * menu_item.height
            pos_x = (self.screen_width / 2) - (menu_item.width / 2)
            pos_y = (self.screen_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

    def render(self):
        for item in self.items:
            if item.is_mouse_over(pygame.mouse.get_pos()):
                item.set_font_color((34, 255, 17))
            else:
                item.set_font_color((255, 255, 255))
            self.screen.blit(item.label, item.position)
        pygame.display.get_surface().blit(self.screen, (0, 0))

    def click(self, event):
        mpos = event.pos
        for item in self.items:
            if item.is_mouse_over(mpos):
                self.funcs[item.text]()

    def loop(self):
        pass
