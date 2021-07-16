from src import common
from src import utils
from src.Engine.objects import game_data

import pygame
import random

pygame.init()


class ShopSubstate:
    def __init__(self, screen=common.SCREEN):
        self.screen = screen
        self.rand_num = random.randint(1, 100000000)

    def draw(self):
        self.screen.fill((0, 255, 0))

        shop_txt = utils.font(80).render("Shop", True, (0, 0, 0))
        shop_txt_rect = shop_txt.get_rect(center=(common.WIDTH // 2, 40))
        self.screen.blit(shop_txt, shop_txt_rect)

        self.screen.blit(utils.font(80).render(str(self.rand_num), True, (0, 0, 0)), (100, 100))

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F7:
                game_data.player = game_data.player_list["main_player"]
                game_data.current_substate = game_data.playing_substate

                game_data.player.x1 = 200
                game_data.player.change = [0, 0]

                game_data.player.move_up = False
                game_data.player.move_down = False
                game_data.player.move_left = False
                game_data.player.move_right = False
