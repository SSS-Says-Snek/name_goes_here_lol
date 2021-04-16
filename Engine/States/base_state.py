from common import *
from Engine.other import *


class BaseState:
    def __init__(self, screen=SCREEN):
        self.screen = screen
        self.font = pygame.font.Font(PATH / "Assets/Fonts/ThaleahFat.ttf", 60)

    def draw(self):
        """Override this function while inheriting from this class"""
        raise GameException("State class must override this function")

    def handle_events(self, event):
        """Override this function while inheriting from this class"""
        raise GameException("State class must override this function")

    def change_state(self, other_state):
        """Override this function while inheriting from this class"""
        raise GameException("State class must override this function")


class DummyState:
    def __init__(self, screen=SCREEN):
        self.screen = screen
        self.font = pygame.font.Font(PATH / "Assets/Fonts/ThaleahFat.ttf", 60)

    def draw(self):
        """Override this function while inheriting from this class"""
        pass

    def handle_events(self, event):
        """Override this function while inheriting from this class"""
        pass

    # def change_state(self, other_state):
    #     """Override this function while inheriting from this class"""
    #     pass
