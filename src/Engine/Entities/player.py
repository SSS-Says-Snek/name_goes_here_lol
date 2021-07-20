"""
This file stores all player classes (E.g main player, shop player, etc)
Each player inherits from BaseEntity, which means that the following methods are required:
    - XEntity.draw()
    - XEntity.handle_events(event)
As usual, there is also XEntity.constant_run(), but of course, it's optional, and not every
entity needs that
"""

import random
import time

from src import common
from src.Engine.base import BaseEntity
from src.Engine.objects import game_data
from src.Engine.Entities.Weapons.guns import BasicGun

import pygame

pygame.init()


class Player(BaseEntity):
    def __init__(self, screen=common.SCREEN):
        super().__init__(screen)

        self.key = None  # Default: No orientation

        self.player = []  # Default: Empty list
        self.player_length = 10  # Default: 10 segments
        self.player_speed = 8  # Default: 8 Pixels per frame
        self.pos = [common.WIDTH // 2, common.HEIGHT // 2]
        self.bullets = []  # Default: No bullets shot yet
        self.inventory = [BasicGun()]  # Default: No items in inventory (yet)
        self.inventory_idx = 0
        self.weapon_last_fired = None

        # Self-explanatory
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False

        self.holding_key = False
        self.redraw_body = True
        self.camera_pos = self.pos[:]

        self.change = (0, 0)  # Default: Stationary
        self.food_rect = self.generate_food()  # Default: Random position of food

    def draw(self):
        self.draw_player(self.player)

        pygame.draw.rect(
            self.screen,
            (128, 128, 128),
            [
                self.pos[0] - game_data.camera_offset[0],
                self.pos[1] - game_data.camera_offset[1],
                20,
                20,
            ],
        )

        pygame.draw.rect(
            self.screen,
            (255, 0, 0),
            [
                self.food_rect[0] - game_data.camera_offset[0],
                self.food_rect[1] - game_data.camera_offset[1],
                self.food_rect[2],
                self.food_rect[3],
            ],
        )

        for bullet in self.bullets:
            bullet.draw_bullet()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and self.key != "left":
                self.key = "right"
                self.change = [self.player_speed, 0]
                self.move_right = True
            if event.key == pygame.K_LEFT and self.key != "right":
                self.key = "left"
                self.change = [-self.player_speed, 0]
                self.move_left = True
            if event.key == pygame.K_UP and self.key != "down":
                self.key = "up"
                self.change = [0, -self.player_speed]
                self.move_up = True
            if event.key == pygame.K_DOWN and self.key != "up":
                self.key = "down"
                self.change = [0, self.player_speed]
                self.move_down = True

            if event.key == pygame.K_SPACE:
                if (self.weapon_last_fired is None) or (
                    time.time() - self.weapon_last_fired
                    > self.inventory[self.inventory_idx].cooldown
                ):
                    self.inventory[self.inventory_idx].fire()
                    self.weapon_last_fired = time.time()

            self.holding_key = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.move_right = False
            if event.key == pygame.K_LEFT:
                self.move_left = False
            if event.key == pygame.K_UP:
                self.move_up = False
            if event.key == pygame.K_DOWN:
                self.move_down = False
            self.change = [0, 0]
            self.holding_key = False

    def constant_run(self):
        self.handle_bullets()

        player_rect = pygame.Rect(self.pos + [20, 20])
        if self.change != [0, 0] and self.redraw_body:
            self.player.append(player_rect)

            if len(self.player) > self.player_length:
                del self.player[0]

        self.change = [0, 0]

        if self.move_right:
            self.change[0] = self.player_speed
            self.pos[0] += self.player_speed
        elif self.move_left:
            self.change[0] = -self.player_speed
            self.pos[0] -= self.player_speed
        elif self.move_up:
            self.change[1] = -self.player_speed
            self.pos[1] -= self.player_speed
        elif self.move_down:
            self.change[1] = self.player_speed
            self.pos[1] += self.player_speed

        self.camera_pos[0] += self.change[0]
        self.camera_pos[1] += self.change[1]

        player_rect = pygame.Rect(self.pos + [20, 20])

        for segment in self.player[:-1]:
            if segment == player_rect:
                print("You collided with yourself. Bruh momento")

        if self.food_rect.colliderect(player_rect):
            self.food_rect = self.generate_food()
            self.player_length += 10
            game_data.player_money += 10 + random.randint(0, 8)

        game_data.camera_offset[0] += (
            self.change[0] - game_data.camera_offset[0] - 410 + self.pos[0]
        ) // 20
        game_data.camera_offset[1] += (
            self.change[1] - game_data.camera_offset[1] - 310 + self.pos[1]
        ) // 20

        prev_segment = None

        for i, segment in enumerate(self.player):
            try:
                if (
                    abs(segment.x - prev_segment.x) not in [self.player_speed, 0]
                    or abs(segment.y - prev_segment.y) not in [self.player_speed, 0]
                ) and (
                    abs(segment.x - prev_segment.x) not in [self.player_speed * 2, 0]
                    or abs(segment.y - prev_segment.y) not in [self.player_speed * 2, 0]
                ):
                    print(f"Detektid at {prev_segment} to {segment}")
                    print(f"Player rect: {self.player}")
                    del self.player[: i + 1]
                    self.player_length = i
            except AttributeError:
                pass

            prev_segment = segment

    def draw_player(self, player_list):
        for i, pos in enumerate(player_list):
            pygame.draw.rect(
                self.screen,
                (0, 0, 0),
                [
                    pos[0] - game_data.camera_offset[0],
                    pos[1] - game_data.camera_offset[1],
                    pos[2],
                    pos[3],
                ],
            )

    def handle_bullets(self):
        for bullet in list(self.bullets):
            bullet.update()

            if bullet.current_lifespan > bullet.lifespan:
                self.bullets.remove(bullet)

    @staticmethod
    def generate_food():
        return pygame.Rect(
            random.randint(0, common.WIDTH - 20),
            random.randint(0, common.HEIGHT - 20),
            20,
            20,
        )


class ShopPlayer(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.player_speed = 5

    def draw(self):
        pygame.draw.rect(self.screen, (128, 128, 128), self.pos + [20, 20])
