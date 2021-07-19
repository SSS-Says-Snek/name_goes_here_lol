from src import common


class BasicGun:
    """Basic gun, only shoots in four directions."""

    def __init__(self, entity, entity_to_shoot, screen=common.SCREEN):
        self.entity = entity  # Could be player, could even be enemy
        self.entity_to_shoot = entity_to_shoot
        self.screen = screen

    def draw(self):
        pass

    def fire(self):
        try:
            self.entity.bullets.append()
        except AttributeError:
            self.entity.bullets
