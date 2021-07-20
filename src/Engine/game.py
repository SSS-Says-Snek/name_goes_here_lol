"""
This file stores the actual game class, used to run the game in main.py
=============================  U S A G E  =============================
>>> from src.Engine.game import GameLoop
>>> game_loop = GameLoop()
>>> game_loop.run()

Note that GameLoop should ONLY be run inside main.py, and no where else. I just wanna make main.py look cool
Cool as in, "My main.py has only 4 lines of code."
"""

from src import common
from src import utils
from src.Engine.States.state import MenuState
from src.Engine.States.debug_game import DebugGame

import time
import os
import psutil
import arrow

import pygame
import pygame_gui

# Initialize pygame submodules
pygame.init()


class GameLoop:
    """Class that stores and runs the game"""

    def __init__(self, screen=common.SCREEN):
        """Initializes some class attributes first"""
        self.screen = screen
        self.manager = pygame_gui.UIManager(
            (common.WIDTH, common.HEIGHT)
        )
        self.clock = pygame.time.Clock()
        self.font = utils.load_font(60)
        self.running = True

        self.state = MenuState(self)
        self.debug_game = DebugGame()
        self.process = psutil.Process(os.getpid())
        self.start_time = arrow.get(time.time())

        self.fps_setting = utils.load_setting("fps")

        pygame.display.set_caption(common.TITLE)

    def run(self):
        """This function runs the actual game loop"""
        # Initializes default variables for debug screen
        loop = 0
        fps = self.clock.get_fps()
        cpu = self.process.cpu_percent()
        mem = (self.process.memory_info().rss, psutil.virtual_memory().used)
        now = arrow.utcnow()

        # Main game loop
        while self.running:
            dt = self.clock.tick(self.fps_setting) / 1000
            self.screen.fill((245, 245, 245))

            # Handles state methods
            self.state.constant_run()
            self.handle_events()
            self.state.draw()

            # Every 30/fps seconds, update debug screen
            if loop % 30 == 1:
                fps = self.clock.get_fps()
                cpu = self.process.cpu_percent()
                mem = (self.process.memory_info().rss, psutil.virtual_memory().used)
                now = arrow.utcnow()

            # Check if debug screen is on. If so, display the
            if self.debug_game.get_debug_state():
                self.debug_game.draw(
                    information={
                        "state": type(self.state),
                        "fps": fps,
                        "cpu": cpu,
                        "mem": mem,
                        "time": (self.start_time, now),
                    }
                )

            # Do pygame gui stuff
            self.manager.update(dt)
            self.manager.draw_ui(self.screen)

            # Updates pygame screen (Flip could also work)
            pygame.display.update()

            # Checks if the next_state is different than the current state. If it is, change states
            if self.state.__class__ != self.state.next_state:
                print(f"Changed from {self.state.__class__} to {self.state.next_state}")
                self.state = self.state.next_state(self)

            # Increment debug loop
            loop += 1

        # After exiting while loop, quit game
        utils.exit_game()

    def handle_events(self):
        """Function used to handle the game loop's events"""
        for game_event in pygame.event.get():
            self.manager.process_events(game_event)

            # Handle state events
            self.state.handle_events(game_event)

            if game_event.type == pygame.QUIT:
                self.running = False
            if game_event.type == pygame.KEYDOWN:
                # Handles F3 presses for debug screen
                if game_event.key == pygame.K_F3:
                    self.debug_game.toggle_debug()
