import random

from src.Engine.base import BaseEntity
from src.Engine.other import game_data
from src.common import *
from src.utils import *

import pygame
from pygame.locals import *

pygame.init()


class Player(BaseEntity):
    def __init__(self, screen=SCREEN):
        super().__init__(screen)

        self.key = "right"  # Default: Right

        self.player = []  # Default: Empty list
        self.player_length = 1  # Default: 1 segment
        self.x1 = WIDTH // 2  # Default: Starting X position
        self.y1 = HEIGHT // 2  # Default: Starting Y position

        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False

        self.camera_x1 = self.x1
        self.camera_y1 = self.y1

        self.change = (0, 0)  # Default: Right
        self.food_rect = self.generate_food()  # Default: Random position of food

    def draw(self):
        self.draw_player(self.player)
        pygame.draw.rect(self.screen, (128, 128, 128), [self.x1 - game_data.camera_offset[0],
                                                        self.y1 - game_data.camera_offset[1],
                                                        20, 20])
        pygame.draw.rect(self.screen, (255, 0, 0), [self.food_rect[0] - game_data.camera_offset[0],
                                                    self.food_rect[1] - game_data.camera_offset[1],
                                                    self.food_rect[2], self.food_rect[3]])

    def handle_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RIGHT and self.key != "left":
                self.key = "right"
                self.change = (5, 0)
                self.move_right = True
            if event.key == K_LEFT and self.key != "right":
                self.key = "left"
                self.change = (-5, 0)
                self.move_left = True
            if event.key == K_UP and self.key != "down":
                self.key = "up"
                self.change = (0, -5)
                self.move_up = True
            if event.key == K_DOWN and self.key != "up":
                self.key = "down"
                self.change = (0, 5)
                self.move_down = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                self.move_right = False
            if event.key == K_LEFT:
                self.move_left = False
            if event.key == K_UP:
                self.move_up = False
            if event.key == K_DOWN:
                self.move_down = False
            self.change = (0, 0)

        # else:
        # self.food_rect = pygame.Rect(self.food_rect.x - self.change[0], self.food_rect.y - self.change[1], 20, 20)

    def constant_run(self):
        change = [0, 0]

        if self.move_right:
            change[0] = 5
        if self.move_left:
            change[0] = -5
        if self.move_up:
            change[1] = -5
        if self.move_down:
            change[1] = 5
        self.x1 += self.change[0]
        self.y1 += self.change[1]

        self.camera_x1 += self.change[0]
        self.camera_y1 += self.change[1]

        player_rect = pygame.Rect([self.x1, self.y1, 20, 20])
        if self.change != (0, 0):
            self.player.append(player_rect)

            if len(self.player) > self.player_length:
                del self.player[0]

        for segment in self.player[:-1]:
            if segment == player_rect and not (self.x1 == WIDTH - 40 or self.x1 == 20 or self.y1 == HEIGHT - 40 or self.y1 == 20):
                print("You collided with yourself. Bruh momento")

        if self.food_rect.colliderect(player_rect):
            self.food_rect = self.generate_food()
            self.player_length += 10

        game_data.camera_offset[0] += (self.change[0] - game_data.camera_offset[0] - 410 + self.x1) // 20
        game_data.camera_offset[1] += (self.change[1] - game_data.camera_offset[1] - 310 + self.y1) // 20

    def draw_player(self, player_list):
        for pos in player_list:
            pygame.draw.rect(self.screen, (0, 0, 0), [pos[0] - game_data.camera_offset[0], pos[1] - game_data.camera_offset[1], pos[2], pos[3]])
            # pygame.draw.rect(self.screen, (0, 0, 0), pos)

    @staticmethod
    def generate_food():
        return pygame.Rect(
            random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 20, 20
        )


class E(BaseEntity):
    pass
