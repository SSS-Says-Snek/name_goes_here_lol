from src import common
from src.Engine.objects import game_data

import math
import pygame

pygame.init()


class Bullet:
    def __init__(self, angle, speed, lifespan, x, y, screen=common.SCREEN):
        self.angle = (
            angle  # Default angle for the bullet: MAY CHANGE FOR DIFFERENT BULLETS
        )
        self.speed = (
            speed  # Default speed for the bullet: MAY CHANGE FOR DIFFERENT BULLETS
        )
        self.lifespan = lifespan * game_data.game_fps  # Default lifespan, in frames

        self.unadjusted_x = x
        self.unadjusted_y = y
        self.x = self.unadjusted_x
        self.y = self.unadjusted_y

        self.screen = screen
        self.current_lifespan = 0
        self.start_cam_offset = game_data.camera_offset[:]

    def update(self):
        self.unadjusted_x += math.sin(self.angle + math.radians(90)) * self.speed
        self.unadjusted_y += math.cos(self.angle + math.radians(90)) * self.speed
        self.current_lifespan += 1

        self.x = (
            self.unadjusted_x - game_data.camera_offset[0] + self.start_cam_offset[0]
        )
        self.y = (
            self.unadjusted_y - game_data.camera_offset[1] + self.start_cam_offset[1]
        )

    def draw_bullet(self):
        pygame.draw.rect(self.screen, (100, 100, 100), [self.x, self.y, 20, 20])

    def on_death(self):
        """Override this if the custom bullet doese something on death of bullet"""


class HomingBullet(Bullet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        super().update()

        self.angle = (
                math.atan2(
                    self.x - game_data.player.pos[0] + game_data.camera_offset[0],
                    self.y - game_data.player.pos[1] + game_data.camera_offset[1],
                )
                + math.radians(90)
        )

    def on_death(self):
        pass
