from src.Engine.States.base_state import BaseState
from src.common import *
from src.utils import *
from src.Engine.button import MenuButton

# from .state import MenuState

import pygame
from pygame.locals import *

pygame.init()


class PauseMenu(BaseState):
    def __init__(
        self,
        game_class,
        screen=SCREEN,
    ):
        super().__init__(game_class)

        self.screen = screen
        self.draw_pause = False

        self.screen_surf = pygame.Surface(self.screen.get_size())  # lgtm [py/call/wrong-arguments]
        self.buttons = {
            "resume_button": (
                MenuButton(
                    self.screen,
                    (300, 200, 200, 100),
                    (128, 128, 128),
                    "Resume",
                    (0, 0, 0),
                    40,
                ),
                lambda: self.toggle_menu(),
            ),
            "quit_button": (
                MenuButton(
                    self.screen,
                    (300, 400, 200, 100),
                    (128, 128, 128),
                    "Quit Game",
                    (0, 0, 0),
                    40,
                ),
                lambda: None,  # self.change_state(MenuState)
            ),
        }
        self.alpha = 1
        self.max_alpha = 180

    def draw(self):
        if self.draw_pause:
            if self.alpha < self.max_alpha:
                self.fade(self.alpha)
            pause_txt = font(60).render("Paused", True, (0, 0, 0))
            self.screen.blit(pause_txt, (300, 100))
            self.screen.blit(self.screen_surf, (0, 0))

            for button in self.buttons.values():
                button[0].draw()

    def fade(self, alpha):
        self.screen_surf.set_alpha(alpha)
        self.alpha += 40

    def handle_events(self, event):
        if self.draw_pause:
            mousex, mousey = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONDOWN:
                for button in self.buttons.values():
                    if button[0].get_rect().collidepoint((mousex, mousey)):
                        button[1]()

    def toggle_menu(self):
        self.draw_pause = not self.draw_pause
        self.alpha = 0
