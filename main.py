import pygame
import cevent
import Menu
import Loader
import tribegame
from pygame.locals import *
from GameResources import *

class GameApp(cevent.CEvent):
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.game = None
        self.size = self.width, self.height = SCREEN_SIZE
        self.clock = pygame.time.Clock()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        #Pre-loading goes here!
        #Perhaps a loading screen sometime down the line?
        #Test Code
        funcs = {'New Game': self.start_game,
                 'Quit': self.on_exit}
        self.game = Menu.StringMenu("Resources/BlackMenu.png", ['New Game', 'Quit'], funcs)
        #End Test Code

    def start_game(self):
        self.game = Loader.load_for_tribegame()

    def on_event(self, event):
        if event.type == QUIT:
            self.on_exit()

        elif event.type >= USEREVENT:
            self.on_user(event)

        elif event.type == VIDEOEXPOSE:
            self.on_expose()

        elif event.type == VIDEORESIZE:
            self.on_resize(event)

        elif event.type == KEYUP:
            self.on_key_up(event)

        elif event.type == KEYDOWN:
            self.on_key_down(event)

        elif event.type == MOUSEMOTION:
            self.on_mouse_move(event)

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.on_lbutton_up(event)
            elif event.button == 2:
                self.on_mbutton_up(event)
            elif event.button == 3:
                self.on_rbutton_up(event)
            else:
                self.on_mouse_wheel(event)

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.on_lbutton_down(event)
            elif event.button == 2:
                self.on_mbutton_down(event)
            elif event.button == 3:
                self.on_rbutton_down(event)
            else:
                self.on_mouse_wheel(event)

        elif event.type == ACTIVEEVENT:
            if event.state == 1:
                if event.gain:
                    self.on_mouse_focus()
                else:
                    self.on_mouse_blur()
            elif event.state == 2:
                if event.gain:
                    self.on_input_focus()
                else:
                    self.on_input_blur()
            elif event.state == 4:
                if event.gain:
                    self.on_restore()
                else:
                    self.on_minimize()

    def on_loop(self):
        self.game.loop()
    def on_render(self):
        self.game.render(self._display_surf)
        pygame.display.flip()
    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            ms = clock.tick(60)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def on_exit(self):
        self._running = False

    def on_lbutton_down(self, event):
        self.game.click(event)

    def on_key_down(self, event):
        if event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN) and isinstance(self.game, tribegame.TribeGame):
            self.game.key_down(event.key)

    def on_key_up(self, event):
        if event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN) and isinstance(self.game, tribegame.TribeGame):
            self.game.key_up(event.key)

if __name__ == "__main__":
    mainApp = GameApp()
    mainApp.on_execute()
