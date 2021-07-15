from src import common
from src import utils
from src.Engine.Entities.player import ShopPlayer
from src.Engine.base import BaseEntity
from src.Engine.objects import TextMessage, game_data
from src.Engine.States import substates

import pygame
import random


class ShopEntity(BaseEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_shop_pos = [
            random.randint(0, common.WIDTH),
            random.randint(0, common.HEIGHT),
        ]
        self.shop_pos = self.start_shop_pos[:]

        self.text_message = TextMessage(
            (20, 400),
            760,
            190,
            (128, 128, 128),
            "Are you sure you want to enter the shop? (Enter to enter shop, move away to exit)",
            utils.font(50),
            instant_blit=False,
            border_color=(80, 80, 80),
            border_width=10,
        )
        self.draw_text_message = False

    def draw(self):
        pygame.draw.rect(
            self.screen, (0, 0, 128), [self.shop_pos[0], self.shop_pos[1], 60, 60]
        )

        if self.draw_text_message:
            self.text_message.draw()

    def handle_events(self, event):
        pass

    def constant_run(self):
        self.shop_pos[0] = self.start_shop_pos[0] - game_data.camera_offset[0]
        self.shop_pos[1] = self.start_shop_pos[1] - game_data.camera_offset[1]

        if pygame.Rect(
            game_data.player.x1 - game_data.camera_offset[0],
            game_data.player.y1 - game_data.camera_offset[1],
            20,
            20,
        ).colliderect(pygame.Rect(self.shop_pos[0], self.shop_pos[1], 60, 60)):
            self.draw_text_message = True
        else:
            self.draw_text_message = False
            self.text_message.reset_current_text()
            # game_data.current_substate = substates.ShopSubstate()
            # shop_player = ShopPlayer()
            # game_data.player = shop_player
            # game_data.player_list["shop_player"] = shop_player
