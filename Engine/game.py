"""This file stores the actual game class, used to run the game in main.py"""

import utils
from common import *
from Engine.States.state import *
from Engine.debug_game import DebugGame
from Engine.other import PopUpMessage

import sys

import pygame
import pygame_gui
from pygame.locals import *

# Initialize pygame submodules
pygame.font.init()
pygame.init()


class GameLoop:
    """Class that stores and runs the game"""
    def __init__(self, screen=SCREEN):
        self.screen = screen
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
        e = font(20)
        print(repr(e))
        # self.uh = PopUpMessage((200, 200, 400, 200), rect_color=(128, 128, 128), text="pafiohpiofhoadhfpadh ofiahpofiapiasdhpos idfhpafhoasdhfpo asdiohfaphiofdhofpasafidhofhops dfhpiosdhfoiasdhpfoiasdhpofisdha ipofhosdfhosdfiasdpofhasdpfohpoasdfhopiasdi hofpahiposdfhi afhopiashfoip", text_font=e)
        self.debug_game = DebugGame()
        pygame.display.set_caption(TITLE)

    def run(self):
        """This function runs the actual game loop"""
        while True:
            dt = self.clock.tick(30) / 1000
            self.screen.fill((245, 245, 245))
            self.handle_events()

            self.state.draw()
            # self.uh.draw()
            
            if self.debug_game.get_debug_state():
                self.debug_game.draw(information={"state": type(self.state)})

            self.manager.update(dt)
            self.manager.draw_ui(self.screen)
            pygame.display.update()

            if self.state.__class__ != self.state.next_state:
                print(f"Changed from {self.state.__class__} to {self.state.next_state}")
                self.state = self.state.next_state()

    def handle_events(self):
        """Function used to handle the game loop's events"""
        for game_event in pygame.event.get():
            self.manager.process_events(game_event)
            self.state.handle_events(game_event)
            if game_event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if game_event.type == KEYDOWN:
                if game_event.key == K_F3:
                    self.debug_game.toggle_debug()
            if game_event.type == USEREVENT:
                # Pygame GUI's event handler
                if game_event.user_type == 'ui_button_pressed':
                    if game_event.ui_element == self.hello_button:
                        self.state.next_state = StatState
                if game_event.user_type == 'ui_drop_down_menu_changed':
                    print("Selected option:", game_event.text)
