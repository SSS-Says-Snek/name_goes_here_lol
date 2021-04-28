from src.common import *
from src.Engine.other import *

from os.path import join


class BaseState(object):
    """
    The base state for other states to inherit from. This class contains:
    - self.screen, used to manage the screen
    - self.font, used to display and render text
    Inherited classes MUST override `draw` and `handle_events`, or else it would raise a GameException
    """
    def __init__(self, screen=SCREEN):
        """
        Note: self.buttons is a dictionary of buttons MADE IN BUTTONS.PY.
        To display other things (E.g pygame_gui's elements), manually draw them instead of putting them in the
        dictionary
        """
        self.screen = screen  # sets the screen to be the default screen
        self.font = pygame.font.Font(join(PATH, "src/Assets/Fonts/ThaleahFat.ttf"), 60)  # sets default font
        self.next_state = self.__class__

    def draw(self):
        """Override this function while inheriting from this class"""
        raise GameException("State class must override this function")

    def handle_events(self, event):
        """Override this function while inheriting from this class"""
        raise GameException("State class must override this function")

    def change_state(self, other_state):
        """No need to override this, this is literally it"""
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
