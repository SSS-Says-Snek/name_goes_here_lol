from src.common import *
from src.utils import *
from src.Engine.other import GameException


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
        self.font = font(60)  # sets default font
        self.next_state = self.__class__  # sets the default state, next_state would change when changing states

    def draw(self):
        """
        Override this function while inheriting from this class
        This function is supposed to be overrided, but the purpose of this function is to draw the state onto the screen.
        This should not be called anywhere except in game.py, where run() would call it via self.state.
        USAGE:
        >>> state = BaseState()  # Supposed to be something that overrided this function
        >>> state.draw()
        <Draws onto screen based on overrided function>
        """
        raise GameException("State class must override this function.\n"
                            "To see more information, check the docstring in base_state.BaseState.draw.")

    def handle_events(self, event):
        """
        Override this function while inheriting from this class
        This function is supposed to be overrided, but the purpose of this function is to provide logic for the state.
        handle_events() handles all the events of pygame, like key presses, mouse clicks, et cetera,
        though some are already found in the run() function in game.py, like window closing.
        This should not be called anywhere except in game.py, where run() would call it via self.state.
        USAGE:
        >>> state = BaseState()  # Supposed to be something that overrided this function
        >>> state.handle_events(event)
        """
        raise GameException("State class must override this function.\n"
                            "To see more information, check the docstring in base_state.BaseState.handle_events.")

    def change_state(self, other_state):
        """
        No need to override this, this is literally it
        change_state() is used when a state wants to change into another state. It changes self.next_state into the desired state
        """
        self.next_state = other_state


class DummyState:
    """Exactly like BaseState, but doesn't raise an exception when not overrided"""
    def __init__(self, screen=SCREEN):
        self.screen = screen
        self.font = font(60)
        self.next_state = self.__class__

    def draw(self):
        """Override this function while inheriting from this class"""
        pass

    def handle_events(self, event):
        """Override this function while inheriting from this class"""
        pass

    def change_state(self, other_state):
        """Override this function while inheriting from this class"""
        pass