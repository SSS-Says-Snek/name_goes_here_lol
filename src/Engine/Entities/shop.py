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
        self.shop_rect = pygame.Rect(self.shop_pos[0], self.shop_pos[1], 60, 60)
        self.shop_collision = [None for _ in range(9)]
        self.shop_state = substates.ShopSubstate()

        self.text_message = TextMessage(
            (20, 400),
            760,
            190,
            (128, 128, 128),
            "Are you sure you want to enter the shop? (Enter to enter shop, move away to exit)",
            utils.load_font(50),
            instant_blit=False,
            border_color=(80, 80, 80),
            border_width=10,
        )
        self.player_collide = False

        self.do_collision = False  # Let's not do it for now :kekw:

    def draw(self):
        pygame.draw.rect(
            self.screen, (0, 0, 128), [self.shop_pos[0], self.shop_pos[1], 60, 60]
        )

        if self.player_collide:
            self.text_message.draw()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_RETURN
                and self.player_collide
                and self.text_message.is_finished
            ):
                game_data.current_substate = self.shop_state
                shop_player = ShopPlayer()
                game_data.player = shop_player
                game_data.player_list["shop_player"] = shop_player

            self.text_message.handle_events(event)

    def constant_run(self):
        self.shop_pos[0] = self.start_shop_pos[0] - game_data.camera_offset[0]
        self.shop_pos[1] = self.start_shop_pos[1] - game_data.camera_offset[1]

        player_rect = pygame.Rect(
            game_data.player.pos[0] - game_data.camera_offset[0],
            game_data.player.pos[1] - game_data.camera_offset[1],
            20,
            20,
        )
        self.shop_rect = pygame.Rect(self.shop_pos[0], self.shop_pos[1], 60, 60)

        if player_rect.colliderect(self.shop_rect):
            self.check_collision(player_rect)
            self.player_collide = True

            if self.do_collision:
                if abs(self.shop_rect.right - player_rect.left) < game_data.player.player_speed and game_data.player.change[0] < 0:
                    print('right')
                    player_rect.left = self.shop_rect.right
                    game_data.player.redraw_body = False
                if abs(self.shop_rect.left - player_rect.right) < game_data.player.player_speed and game_data.player.change[0] > 0:
                    print('left')
                    player_rect.right = self.shop_rect.left
                    game_data.player.redraw_body = False
                if abs(self.shop_rect.top - player_rect.bottom) < game_data.player.player_speed and game_data.player.change[1] > 0:
                    print('top')
                    player_rect.bottom = self.shop_rect.top
                    game_data.player.redraw_body = False
                if abs(self.shop_rect.bottom - player_rect.top) < game_data.player.player_speed and game_data.player.change[1] < 0:
                    print('bottom')
                    player_rect.top = self.shop_rect.bottom
                    game_data.player.redraw_body = False

                player_rect.x -= game_data.player.change[0]
                player_rect.y -= game_data.player.change[1]

                game_data.player.pos = [player_rect.x + game_data.camera_offset[0], player_rect.y + game_data.camera_offset[1]]
        elif (
                self.do_collision and
                utils.distance(self.shop_rect.centerx, player_rect.centerx, self.shop_rect.centery, player_rect.centery) <= 100
        ):
            self.player_collide = True
        else:
            self.player_collide = False
            game_data.player.redraw_body = True
            self.text_message.reset_current_text()

    def check_collision(self, rect):
        self.shop_collision[0] = rect.collidepoint(self.shop_rect.topleft)
        self.shop_collision[1] = rect.collidepoint(self.shop_rect.topright)
        self.shop_collision[2] = rect.collidepoint(self.shop_rect.bottomleft)
        self.shop_collision[3] = rect.collidepoint(self.shop_rect.bottomright)

        self.shop_collision[4] = rect.collidepoint(self.shop_rect.midleft)
        self.shop_collision[5] = rect.collidepoint(self.shop_rect.midright)
        self.shop_collision[6] = rect.collidepoint(self.shop_rect.midtop)
        self.shop_collision[7] = rect.collidepoint(self.shop_rect.midbottom)

        self.shop_collision[8] = rect.collidepoint(self.shop_rect.center)
