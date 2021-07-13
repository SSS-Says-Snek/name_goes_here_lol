from src import common
from src.Engine.base import BaseEnemy
from src.Engine.objects import game_data

import random
import math
import pygame

pygame.init()


class Bullet:
    def __init__(self, angle, speed, lifespan, x, y, screen=common.SCREEN):
        self.angle = angle
        self.speed = speed
        self.lifespan = lifespan * game_data.game_fps
        self.x = x
        self.y = y
        self.screen = screen
        self.current_lifespan = 0

    def update(self):
        self.x += math.sin(self.angle + math.radians(90)) * self.speed
        self.y += math.cos(self.angle + math.radians(90)) * self.speed
        self.current_lifespan += 1

    def draw_bullet(self):
        pygame.draw.rect(self.screen, (100, 100, 100), [self.x, self.y, 20, 20])


class BulletEnemy(BaseEnemy):
    def __init__(self, player_obj, screen=common.SCREEN):
        super().__init__(player_obj, screen)

        self.start_pos = (random.randint(0, common.WIDTH), random.randint(0, common.HEIGHT))
        self.enemy_pos = self.start_pos
        self.bullets = []
        self.firing_speed = 5.5
        self.bullet_speed = 7

        self.FIREBULLET = pygame.USEREVENT + 2

        pygame.time.set_timer(self.FIREBULLET, int(self.firing_speed * 1000))

    def draw(self):
        pygame.draw.rect(
            self.screen, (180, 180, 180), (self.enemy_pos[0], self.enemy_pos[1], 40, 40)
        )

        for bullet in self.bullets:
            bullet.draw_bullet()

    def handle_events(self, event):
        if event.type == self.FIREBULLET:
            bullet_rad = (
                math.atan2(
                    self.enemy_pos[0] - self.player_obj.x1 + game_data.camera_offset[0],
                    self.enemy_pos[1] - self.player_obj.y1 + game_data.camera_offset[1],
                )
                + math.radians(90)
            )
            print(
                f"Enemy: {self.enemy_pos}, Player: {self.player_obj.x1, self.player_obj.y1}"
            )
            print(math.degrees(bullet_rad))

            self.bullets.append(
                Bullet(bullet_rad, self.bullet_speed, 10, *self.enemy_pos)
            )

    def constant_run(self):
        self.enemy_pos = (
            self.start_pos[0] - game_data.camera_offset[0],
            self.start_pos[1] - game_data.camera_offset[1],
        )

        for bullet in list(self.bullets):
            bullet.update()
            # if (not 0 < bullet.x < 5600) or (not 0 < bullet.y < 4200):
            #     self.bullets.remove(bullet)
            if bullet.current_lifespan > bullet.lifespan:
                self.bullets.remove(bullet)

            for i, part in enumerate(reversed(list(self.player_obj.player))):
                if pygame.Rect(
                    bullet.x + game_data.camera_offset[0],
                    bullet.y + game_data.camera_offset[1],
                    20,
                    20,
                ).colliderect(part):
                    try:
                        print(f"Hit, at {part.x, part.y} (Real: {bullet.x, bullet.y}")
                        self.player_obj.player = self.player_obj.player[:i]
                        print("PLAYER LST", self.player_obj.player)
                        self.player_obj.player_length = len(self.player_obj.player)
                        self.bullets.remove(bullet)
                        break
                    except ValueError:
                        continue
