import random

from src import common
from src.Engine.base import BaseEntity
from src.Engine.objects import game_data

import pygame

pygame.init()


class Player(BaseEntity):
    def __init__(self, screen=common.SCREEN):
        super().__init__(screen)

        self.key = None  # Default: No orientation

        self.player = []  # Default: Empty list
        self.player_length = 10  # Default: 10 segments
        self.x1 = common.WIDTH // 2  # Default: Starting X position
        self.y1 = common.HEIGHT // 2  # Default: Starting Y position

        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False
        self.holding_key = False

        self.camera_x1 = self.x1
        self.camera_y1 = self.y1

        self.change = (0, 0)  # Default: Stationary
        self.food_rect = self.generate_food()  # Default: Random position of food

    def draw(self):
        self.draw_player(self.player)
        pygame.draw.rect(
            self.screen,
            (128, 128, 128),
            [
                self.x1 - game_data.camera_offset[0],
                self.y1 - game_data.camera_offset[1],
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

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and self.key != "left" and not self.holding_key:
                self.key = "right"
                self.change = (5, 0)
                self.move_right = True
            elif event.key == pygame.K_LEFT and self.key != "right" and not self.holding_key:
                self.key = "left"
                self.change = (-5, 0)
                self.move_left = True
            elif event.key == pygame.K_UP and self.key != "down" and not self.holding_key:
                self.key = "up"
                self.change = (0, -5)
                self.move_up = True
                print('up')
            elif event.key == pygame.K_DOWN and self.key != "up" and not self.holding_key:
                self.key = "down"
                self.change = (0, 5)
                self.move_down = True
            self.holding_key = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.move_right = False
            elif event.key == pygame.K_LEFT:
                self.move_left = False
            elif event.key == pygame.K_UP:
                self.move_up = False
            elif event.key == pygame.K_DOWN:
                self.move_down = False
            self.change = (0, 0)
            self.holding_key = False

        # else:
        # self.food_rect = pygame.Rect(self.food_rect.x - self.change[0], self.food_rect.y - self.change[1], 20, 20)

    def constant_run(self):
        change = [0, 0]

        if self.move_right:
            change[0] = 10
            self.x1 += 10
        elif self.move_left:
            change[0] = -10
            self.x1 -= 10
        elif self.move_up:
            change[1] = -10
            self.y1 -= 10
        elif self.move_down:
            change[1] = 10
            self.y1 += 10

        self.camera_x1 += change[0]
        self.camera_y1 += change[1]

        player_rect = pygame.Rect([self.x1, self.y1, 20, 20])

        if change != [0, 0]:
            self.player.append(player_rect)

            if len(self.player) > self.player_length:
                del self.player[0]

        for segment in self.player[:-1]:
            if segment == player_rect:
                print("You collided with yourself. Bruh momento")

        if self.food_rect.colliderect(player_rect):
            self.food_rect = self.generate_food()
            self.player_length += 10

        game_data.camera_offset[0] += (
            self.change[0] - game_data.camera_offset[0] - 410 + self.x1
        ) // 20
        game_data.camera_offset[1] += (
            self.change[1] - game_data.camera_offset[1] - 310 + self.y1
        ) // 20

    def draw_player(self, player_list):
        for pos in player_list:
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

    @staticmethod
    def generate_food():
        return pygame.Rect(
            random.randint(0, common.WIDTH - 20), random.randint(0, common.HEIGHT - 20), 20, 20
        )
