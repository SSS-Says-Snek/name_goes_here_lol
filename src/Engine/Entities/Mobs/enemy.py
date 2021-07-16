from src import common
from src.Engine.base import BaseEnemy
from src.Engine.objects import game_data
from src.Engine.Entities.Weapons.bullets import Bullet, HomingBullet

import random
import math
import pygame

pygame.init()


class BulletEnemy(BaseEnemy):
    def __init__(self, player_obj, screen=common.SCREEN):
        super().__init__(player_obj, screen)

        self.start_pos = (
            random.randint(0, common.WIDTH),
            random.randint(0, common.HEIGHT),
        )
        self.enemy_pos = self.start_pos
        self.bullets = []
        self.firing_speed = 5.5
        self.bullet_speed = 7
        self.bullet_type = Bullet

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

            # Creates bullet, and appends it to
            self.bullets.append(
                self.bullet_type(bullet_rad, self.bullet_speed, 10, *self.enemy_pos)
            )

    def constant_run(self):
        self.enemy_pos = (
            self.start_pos[0] - game_data.camera_offset[0],
            self.start_pos[1] - game_data.camera_offset[1],
        )
        # print("Outside:", self.player_obj.player)

        for bullet in list(self.bullets):
            bullet.update()
            if bullet.current_lifespan > bullet.lifespan:
                self.bullets.remove(bullet)

            for i, part in enumerate(reversed(list(self.player_obj.player))):
                if pygame.Rect(
                        bullet.x
                        + game_data.camera_offset[0],  # + 2*game_data.camera_offset[0],
                        bullet.y
                        + game_data.camera_offset[1],  # + 2*game_data.camera_offset[1],
                        20,
                        20,
                ).colliderect(part):
                    try:
                        print(f"Hit, at {part.x, part.y} (Real: {bullet.x, bullet.y}")
                        self.player_obj.player = self.player_obj.player[:i]
                        self.player_obj.player_length = i
                        print(self.player_obj.player)

                        change_dict = {"right": [self.player_obj.player_speed, 0], "left": [-self.player_obj.player_speed, 0],
                                       "up": [0, -self.player_obj.player_speed], "down": [0, self.player_obj.player_speed]}

                        self.player_obj.change = change_dict[self.player_obj.key]
                        print(self.player_obj.change)
                        self.bullets.remove(bullet)
                        break
                    except ValueError:
                        continue


class HomingBulletEnemy(BulletEnemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.firing_speed = 8
        self.bullet_speed = 3
        self.bullet_type = HomingBullet

        pygame.time.set_timer(self.FIREBULLET, int(self.firing_speed * 1000))
