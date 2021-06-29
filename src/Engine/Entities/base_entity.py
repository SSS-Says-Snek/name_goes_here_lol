from src.common import *
from src.Engine.other import GameException

import pygame

pygame.init()


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
