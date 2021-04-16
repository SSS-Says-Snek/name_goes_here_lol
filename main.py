"""This is the MAIN FILE used to run the game."""
import utils
from common import *
from button import *
from utils import *
from menu import Menu
from Engine.States.state import *

import sys
import configparser

import pygame
import pygame_gui
from pygame.locals import *

# Initialize pygame submodules
pygame.font.init()
pygame.init()

MENUSTATE = 'main menu'
BUTTON_HOVER_COLOR = None
BUTTON_HOVER = {}


class GameLoop:
    def __init__(self):
        self.screen = SCREEN
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT), PATH / "Assets/Themes/test_theme.json")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(PATH / "Assets/Fonts/ThaLeahFat.ttf", 60)

        self.menu = CurrentState()
        self.hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 500), (100, 50)),
                                                         text='wut',
                                                         manager=self.manager)
        self.test = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(["Test1", "Test2", "TestInfinite"],
                                                                         "Choose pls",
                                                                         relative_rect=pygame.Rect((200, 500), (150, 30)),
                                                                         manager=self.manager)
        pygame.display.set_caption(TITLE)

    def run(self):
        while True:
            dt = self.clock.tick(30) / 1000
            self.screen.fill((245, 245, 245))
            self.handle_events()
            # .draw()
            self.menu.draw()

            txt = utils.font(20).render(repr(self.menu), True, (0, 0, 0))
            self.screen.blit(txt, (400, 440))
            # print(repr(self.menu))

            self.manager.update(dt)
            self.manager.draw_ui(self.screen)
            pygame.display.update()

    def handle_events(self):
        global MENUSTATE, BUTTON_HOVER_COLOR, BUTTON_HOVER
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            self.manager.process_events(event)
            self.menu.handle_events(event)
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == USEREVENT:
                # Pygame GUI's event handler
                if event.user_type == 'ui_button_pressed':
                    if event.ui_element == self.hello_button:
                        MENUSTATE = 'start game'
                if event.user_type == 'ui_drop_down_menu_changed':
                    print("Selected option:", event.text)

        # for key, button in self.menu.buttons.items():
        #     if isinstance(button, Button):
        #         if button.get_rect().collidepoint(mouse_x, mouse_y):
        #             BUTTON_HOVER[key] = (0, 128, 0)
        #         else:
        #             BUTTON_HOVER[key] = None
        #         # if is_hovering(button.get_rect(), (mouse_x, mouse_y)):
        #         #     self.menu.generate_dollar_sign(50, (button.get_rect().right + 100, button.get_rect().centery), (0, 255, 0))
        #     else:
        #         BUTTON_HOVER[key] = None


if __name__ == "__main__":
    game_loop = GameLoop()
    game_loop.run()
