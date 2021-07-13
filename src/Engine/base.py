from src.common import *
from src.utils import *
from src.Engine.objects import GameException

import pygame

pygame.init()


class BaseState(object):
    """
    The base state for other states to inherit from. This class contains:
        - self.screen, used to manage the screen
        - self.font, used to display and render text
        - self.next_state, used to determine the next state of the state
        - self.game_class, used to get information from game.py's GameLoop
    Inherited classes MUST override `draw` and `handle_events`, or else it would raise a GameException
    """

    def __init__(self, game_class, screen=SCREEN):
        """
        Note: self.buttons is a dictionary of buttons MADE IN BUTTONS.PY.
        To display other things (E.g pygame_gui's elements), manually draw them instead of putting them in the
        dictionary
        """
        self.screen = screen  # sets the screen to be the default screen
        self.font = font(60)  # sets default font
        self.next_state = (
            self.__class__
        )  # sets the default state, next_state would change when changing states
        self.game_class = game_class  # Some States may need info on the game class

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
        raise GameException(
            f"State class {self.__class__} must override this function.\n"
            "To see more information, check the docstring in base_state.BaseState.draw."
        )

    def handle_events(self, event):
        """
        Override this function while inheriting from this class
        This function is supposed to be overrided, but the purpose of this function is to provide logic for the state.
        handle_events() handles all the events of pygame, like key presses, mouse clicks, et cetera,
        though some are already found in the run() function in game.py, like window closing.
        This should not be called anywhere except in game.py, where run() would call it via self.state.
        ==========================================  USAGE:  ==========================================
        >>> state = BaseState()  # Supposed to be something that overrided this function
        >>> state.handle_events(event)
        """
        raise GameException(
            f"State class {self.__class__} must override this function.\n"
            "To see more information, check the docstring in base_state.BaseState.handle_events."
        )

    def constant_run(self):
        """
        This function is optional. Do not override if you are not planning to use it
        This function handles anything that will be run *once per frame*, as currently, the only way of doing that
        is via the draw() function, and let's face it, that's plain weird to write non-draw related code in draw()
        This should not be called anywhere except in game.py, where constant_run() would call it via self.state.
        ==========================================  USAGE:  ==========================================
        >>> state = BaseState()  # Supposed to be something that overrided this function
        >>> state.constant_run()
        """
        pass

    def change_state(self, other_state):
        """
        No need to override this, this is literally it
        change_state() is used when a state wants to change into another state. It changes self.next_state into the desired state
        Sometimes, there would be a class inheriting from BaseState, but is actually not a state (E.g pause menu)
        In this case, override change_state with a new function
        ==========================================  USAGE:  ==========================================
        >>> your_state = BaseState()  # IDK I'm just trying to avoid pycharm errors
        >>> your_state.change_state("Other State")
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


class BaseEntity(object):
    """
    The base entity for all entities to inherit from. The base class contains:
        - screen (used to blit objects onto the window)
    Inherited classes MUST override the `draw` and `handle_event` functions, or else it would
    raise a GameException
    """

    def __init__(self, screen=SCREEN):
        """
        Defines several parameters used in entities

        Parameters:
            - screen (default: src.common.SCREEN): Used to blit objects onto the window
        """
        self.screen = screen

    def __str__(self):
        return f"e{self}"

    def draw(self):
        """
        Override this function while inheriting from this class
        This function is supposed to be overrided, but the purpose of this function is to draw the state onto the screen.
        This should usually be called in state.py, as entities are usually defined there. However, there are
        exceptions.
        ==========================================  USAGE:  ==========================================
        >>> entity = BaseEntity()  # Supposed to be something that overrided this function
        >>> entity.draw()
        <Draws onto screen based on overrided function>
        """
        raise GameException(
            f"Entity class {self.__class__} must override draw function\n"
            "To see more information, see base_entity.BaseEntity.draw"
        )

    def handle_events(self, event):
        """
        Override this function while inheriting from this class
        This function is supposed to be overrided, but the purpose of this function is to provide logic for the entity.
        handle_events() handles all the events of pygame, like key presses, mouse clicks, et cetera,
        though some are already found in the run() function in game.py, like window closing.
        This should usually be called in state.py, as entities are usually defined there. However, there are
        exceptions
        ==========================================  USAGE:  ==========================================
        >>> entity = BaseEntity()  # Supposed to be something that overrided this function
        >>> entity.handle_events(event)
        """
        raise GameException(
            f"Entity class {self.__class__} must override handle_events function\n"
            "To see more information, see base_entity.BaseEntity.handle_events"
        )


class BaseEnemy(object):
    def __init__(self, player_obj, screen=SCREEN):
        self.player_obj = player_obj
        self.screen = screen

    def draw(self):
        """
        Override this function while inheriting from this class
        This function is supposed to be overrided, but the purpose of this function is to draw the state onto the screen.
        This should usually be called in state.py, as enemies are usually defined there. However, there are
        exceptions.
        ==========================================  USAGE:  ==========================================
        >>> player = BaseEntity()
        >>> entity = BaseEnemy(player)  # Supposed to be something that overrided this function
        >>> entity.draw()
        <Draws onto screen based on overrided function>
        """
        raise GameException(
            f"Enemy class {self.__class__} must override draw function\n"
            "To see more information, see base_entity.BaseEntity.draw"
        )

    def handle_events(self, event):
        """
        Override this function while inheriting from this class
        This function is supposed to be overrided, but the purpose of this function is to provide logic for the entity.
        handle_events() handles all the events of pygame, like key presses, mouse clicks, et cetera,
        though some are already found in the run() function in game.py, like window closing.
        This should usually be called in state.py, as enemies are usually defined there. However, there are
        exceptions
        ==========================================  USAGE:  ==========================================
        >>> player = BaseEntity()
        >>> entity = BaseEnemy(player)  # Supposed to be something that overrided this function
        >>> entity.handle_events(event)
        """
        raise GameException(
            f"Entity class {self.__class__} must override handle_events function\n"
            "To see more information, see base_entity.BaseEntity.handle_events"
        )
