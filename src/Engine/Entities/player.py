import random

from src.Engine.Entities.base_entity import BaseEntity
# from src.Engine.other import game_data
from src.common import *
from src.utils import *

import pygame
from pygame.locals import *

pygame.init()


class Player(BaseEntity):
    def __init__(self, screen=SCREEN):
        super().__init__(screen)

        self.key = "right"

        self.player = []
        self.player_length = 1
        self.x1 = WIDTH // 2
        self.y1 = HEIGHT // 2
        self.change = (5, 0)
        self.food_rect = self.generate_food()

    def draw(self):
        self.draw_player(self.player)
        pygame.draw.rect(self.screen, (128, 128, 128), [self.x1, self.y1, 20, 20])
        pygame.draw.rect(self.screen, (255, 0, 0), self.food_rect)

    def handle_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RIGHT and self.key != "left":
                self.key = "right"
                self.change = (5, 0)
            if event.key == K_LEFT and self.key != "right":
                self.key = "left"
                self.change = (-5, 0)
            if event.key == K_UP and self.key != "down":
                self.key = "up"
                self.change = (0, -5)
            if event.key == K_DOWN and self.key != "up":
                self.key = "down"
                self.change = (0, 5)

        player_rect = pygame.Rect([self.x1, self.y1, 20, 20])
        self.player.append(player_rect)

        if len(self.player) > self.player_length:
            del self.player[0]

        if self.food_rect.colliderect(player_rect):
            self.food_rect = self.generate_food()
            self.player_length += 10
        # else:
            # self.food_rect = pygame.Rect(self.food_rect.x - self.change[0], self.food_rect.y - self.change[1], 20, 20)

        self.x1 += self.change[0]
        self.y1 += self.change[1]

        # game_data.camera_offset[0] += (self.change[0] - game_data.camera_offset[0] + self.x1) // 1
        # game_data.camera_offset[1] += (self.change[1] - game_data.camera_offset[1] + self.y1) // 1

    def draw_player(self, player_list):
        for pos in player_list:
            if not ((
                    (abs(pos[0] - self.x1) == 5 and pos[1] == self.y1) or
                    (pos[0] == self.x1 and abs(pos[1] - self.y1) == 5)
            )):
                pygame.draw.rect(self.screen, (0, 0, 0), pos)
            else:
                pygame.draw.rect(self.screen, (128, 128, 128), pos)

    @staticmethod
    def generate_food():
        return pygame.Rect(
            random.randint(0, WIDTH), random.randint(0, HEIGHT), 20, 20
        )


class E(BaseEntity):
    pass
