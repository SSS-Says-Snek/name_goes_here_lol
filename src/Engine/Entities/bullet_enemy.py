from src.Engine.Entities.base_entity import BaseEntity
from src.common import *

import random
import math
import pygame

pygame.init()


class Bullet:
    def __init__(self, angle, speed, x, y, screen=SCREEN):
        self.angle = angle
        self.speed = speed
        self.x = x
        self.y = y
        self.screen = screen

    def update(self):
        self.x += math.cos(self.angle + math.radians(90)) * self.speed
        self.y += math.sin(self.angle + math.radians(90)) * self.speed

    def draw_bullet(self):
        pygame.draw.rect(self.screen, (100, 100, 100), [self.x, self.y, 20, 20])


class BulletEnemy(BaseEntity):
    def __init__(self, screen=SCREEN):
        super().__init__(screen)

        self.enemy_pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.bullets = []
        self.firing_speed = 5000
        self.bullet_speed = 11

        self.FIREBULLET = pygame.USEREVENT + 2

        pygame.time.set_timer(self.FIREBULLET, self.firing_speed)

    def draw(self):
        pygame.draw.rect(self.screen, (180, 180, 180), self.enemy_pos + (40, 40))

        for bullet in self.bullets:
            bullet.draw_bullet()

    def handle_events(self, event, player_pos):
        if event.type == self.FIREBULLET:
            bullet_rad = math.atan2(self.enemy_pos[1] - player_pos[1], self.enemy_pos[0] - player_pos[0]) + math.radians(90)
            self.bullets.append(Bullet(bullet_rad, self.bullet_speed, *self.enemy_pos))
        for bullet in list(self.bullets):
            bullet.update()
            if (not 0 < bullet.x < WIDTH) or (not 0 < bullet.y < HEIGHT):
                self.bullets.remove(bullet)
