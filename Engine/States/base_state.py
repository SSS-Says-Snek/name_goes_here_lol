from common import *
from Engine.other import *

from os.path import join


class BaseState(object):
    def __init__(self, screen=SCREEN):
        self.screen = screen
        self.font = pygame.font.Font(join(PATH, "Assets/Fonts/ThaleahFat.ttf"), 60)

    def draw(self):
        """Override this function while inheriting from this class"""
        raise GameException("State class must override this function")

    def handle_events(self, event):
        """Override this function while inheriting from this class"""
        raise GameException("State class must override this function")

    # def change_state(self, other_state):
    #     """Override this function while inheriting from this class"""
    #     raise GameException("State class must override this function")

    def change_state(self, other_state):
        self.next_state = other_state


class DummyState:
    """Exactly like BaseState, but doesn't raise an exception when not overrided"""
    def __init__(self, screen=SCREEN):
        self.screen = screen
        self.font = pygame.font.Font(PATH / "Assets/Fonts/ThaleahFat.ttf", 60)

    def draw(self):
        """Override this function while inheriting from this class"""
        pass

    def handle_events(self, event):
        """Override this function while inheriting from this class"""
        pass

    def change_state(self, other_state):
        """Override this function while inheriting from this class"""
        pass
