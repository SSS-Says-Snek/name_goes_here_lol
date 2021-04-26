from common import *
from utils import *

import pygame


class DebugGame:
    def __init__(self, screen=SCREEN):
        self.screen = screen
        self.draw_debug = False

    def draw(self, information: dict):
        debug_surf = pygame.Surface((350, 200))
        debug_surf.fill((128, 128, 128))

        debug_title_txt = font(50).render("Debug Screen", True, (0, 0, 0))
        debug_title_txt_pos = debug_title_txt.get_rect()
        debug_title_txt_pos.center = (175, 20)
        debug_surf.blit(debug_title_txt, debug_title_txt_pos)

        debug_state_txt = font(16).render(f"State: {information['state']}", True, (0, 0, 0))
        debug_surf.blit(debug_state_txt, (15, 90))

        debug_fps_txt = font(20).render(f"Frames per second: {str(round(information['fps'], 5))}", True, (0, 0, 0))
        debug_surf.blit(debug_fps_txt, (15, 60))

        debug_surf.set_alpha(220)

        self.screen.blit(debug_surf, (0, 0))

    def toggle_debug(self):
        self.draw_debug = not self.draw_debug

    def get_debug_state(self):
        return self.draw_debug
