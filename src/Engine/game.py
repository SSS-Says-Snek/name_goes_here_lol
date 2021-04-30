"""This file stores the actual game class, used to run the game in main.py"""

from src.Engine.States.state import *
from src.Engine.States.debug_game import DebugGame
from src.utils import *

import time
import sys
import os
import psutil
import arrow

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
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT), PATH / "src/Assets/Themes/test_theme.json")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(PATH / "src/Assets/Fonts/ThaleahFat.ttf", 60)

        self.state = MenuState()
        # self.hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 500), (100, 50)),
        #                                                  text='wut',
        #                                                  manager=self.manager)
        # self.test = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(["Test1", "Test2", "TestInfinite"],
        #                                                                  "Choose pls",
        #                                                                  relative_rect=pygame.Rect((200, 500), (150, 30)),
        #                                                                  manager=self.manager)
        self.debug_game = DebugGame()
        self.process = psutil.Process(os.getpid())
        self.start_time = arrow.get(time.time())
        pygame.display.set_caption(TITLE)

    def run(self):
        """This function runs the actual game loop"""
        loop = 0
        fps = self.clock.get_fps()
        cpu = self.process.cpu_percent()
        mem = (self.process.memory_info().rss, psutil.virtual_memory().used)
        now = arrow.utcnow()
        while True:
            dt = self.clock.tick(30) / 1000
            self.screen.fill((245, 245, 245))
            self.handle_events()

            self.state.draw()
            if loop % 30 == 1:
                fps = self.clock.get_fps()
                cpu = self.process.cpu_percent()
                mem = (self.process.memory_info().rss, psutil.virtual_memory().used)
                now = arrow.utcnow()
            if self.debug_game.get_debug_state():
                self.debug_game.draw(
                    information={
                        "state": type(self.state),
                        "fps": fps,
                        "cpu": cpu,
                        "mem": mem,
                        "time": (self.start_time, now)
                    }
                )

            self.manager.update(dt)
            self.manager.draw_ui(self.screen)
            pygame.display.update()

            # Checks if the next_state is different than the current state. If it is, change states
            if self.state.__class__ != self.state.next_state:
                print(f"Changed from {self.state.__class__} to {self.state.next_state}")
                self.state = self.state.next_state()
            loop += 1

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
