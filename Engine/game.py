import utils
from common import *
from Engine.States.state import *

import sys

import pygame
import pygame_gui
from pygame.locals import *

# Initialize pygame submodules
pygame.font.init()
pygame.init()


class GameLoop:
    def __init__(self):
        self.screen = SCREEN
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT), PATH / "Assets/Themes/test_theme.json")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(PATH / "Assets/Fonts/ThaLeahFat.ttf", 60)

        self.state = MenuState()
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

            self.state.draw()

            txt = utils.font(20).render(repr(self.state), True, (0, 0, 0))
            self.screen.blit(txt, (400, 440))

            self.manager.update(dt)
            self.manager.draw_ui(self.screen)
            pygame.display.update()

            if self.state.__class__ != self.state.next_state:
                print(f"Changed from {self.state.__class__} to {self.state.next_state}")
                self.state = self.state.next_state()

    def handle_events(self):
        for game_event in pygame.event.get():
            self.manager.process_events(game_event)
            self.state.handle_events(game_event)
            if game_event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if game_event.type == USEREVENT:
                # Pygame GUI's event handler
                if game_event.user_type == 'ui_button_pressed':
                    if game_event.ui_element == self.hello_button:
                        self.state.next_state = StatState
                if game_event.user_type == 'ui_drop_down_menu_changed':
                    print("Selected option:", game_event.text)