from src import common
from src.Engine.objects import game_data
from src.Engine.Entities.Weapons import bullets

import math


class BasicGun:
    """Basic gun, only shoots in four directions."""

    def __init__(self, screen=common.SCREEN):
        self.screen = screen
        self.damage = 30
        self.bullet_speed = 10
        self.bullet_lifespan = 7
        self.cooldown = 1/3  # 1/3 of a second per shot
        self.orientation = {
            "right": math.radians(0),
            "left": math.radians(180),
            "up": math.radians(90),
            "down": math.radians(-90),
            None: math.radians(0)
        }

    def draw(self):
        pass

    def fire(self):
        angle = self.orientation[game_data.player.key]
        game_data.player.bullets.append(
            bullets.Bullet(
                angle, self.bullet_speed, self.bullet_lifespan,
                game_data.player.pos[0] + game_data.player.change[0] - game_data.camera_offset[0],
                game_data.player.pos[1] + game_data.player.change[1] - game_data.camera_offset[1]
            )
        )
