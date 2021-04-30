from src.utils import *

import pygame


class DebugGame:
    def __init__(self, screen=SCREEN):
        self.screen = screen
        self.draw_debug = False

    def draw(self, information: dict):
        debug_surf = pygame.Surface((400, 230))
        debug_surf.fill((128, 128, 128))

        debug_title_txt = font(50).render("Debug Screen", True, (0, 0, 0))
        debug_title_txt_pos = debug_title_txt.get_rect()
        debug_title_txt_pos.center = (175, 20)
        debug_surf.blit(debug_title_txt, debug_title_txt_pos)

        debug_state_txt = font(16).render(f"State: {information['state']}", True, (0, 0, 0))
        debug_surf.blit(debug_state_txt, (15, 60))

        debug_fps_txt = font(20).render(f"Frames per second: {str(round(information['fps'], 5))}", True, (0, 0, 0))
        debug_surf.blit(debug_fps_txt, (15, 90))

        debug_cpu_txt = font(20).render(f"CPU Percentage: {information['cpu']}%", True, (0, 0, 0))
        debug_surf.blit(debug_cpu_txt, (15, 120))

        debug_mem_txt = font(20).render(f"RAM Taken Up: {format_byte(information['mem'][0])} ({round(information['mem'][0] / information['mem'][1] * 100, 3)}% of {format_byte(information['mem'][1])})",
                                        True, (0, 0, 0))
        debug_surf.blit(debug_mem_txt, (15, 150))

        debug_time_txt = font(20).render(f"Time Played: {information['time'][0].humanize(information['time'][1], only_distance=True)}", True, (0, 0, 0))
        debug_surf.blit(debug_time_txt, (15, 180))

        debug_surf.set_alpha(220)

        self.screen.blit(debug_surf, (0, 0))

    def toggle_debug(self):
        self.draw_debug = not self.draw_debug

    def get_debug_state(self):
        return self.draw_debug
