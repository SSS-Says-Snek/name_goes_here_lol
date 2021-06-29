import random

from src.Engine.Entities.base_entity import BaseEntity
from src.common import *
from src.utils import *

import pygame
from pygame.locals import *

pygame.init()


class Player(BaseEntity):
    def __init__(self, screen=SCREEN):
        super().__init__(screen)

        self.key = "right"

        self.thickness = 20
        self.player = []
        self.player_length = 1
        self.x1 = WIDTH // 2
        self.y1 = HEIGHT // 2
        self.change = (5, 0)
        self.food_rect = None
        self.generate_food()

    def draw(self):
        self.draw_player([20, 20], self.player)
        pygame.draw.rect(self.screen, (128, 128, 128), [self.x1, self.y1, 20, 20])
        pygame.draw.rect(self.screen, (255, 0, 255), self.food_rect)

    def generate_food(self):
        self.food_rect = pygame.Rect(
            random.randint(0, WIDTH), random.randint(0, HEIGHT), 20, 20
        )

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

        player_head = [self.x1, self.y1]
        player_rect = player_head + [20, 20]
        self.player.append(player_head)
        if len(self.player) > self.player_length:
            del self.player[0]

        if self.food_rect.colliderect(player_rect):
            self.generate_food()
            self.player_length += 10

        self.x1 += self.change[0]
        self.y1 += self.change[1]

    def draw_player(self, size, player_list):
        for pos in player_list:
            if not ((abs(pos[0] - self.x1) == 5 and pos[1] == self.y1) or (pos[0] == self.x1 and abs(pos[1] - self.y1) == 5)):
                pygame.draw.rect(self.screen, (0, 0, 0), pos + size)
            else:
                pygame.draw.rect(self.screen, (128, 128, 128), pos + size)


class E(BaseEntity):
    pass
