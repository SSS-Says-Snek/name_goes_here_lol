from src.common import *

import pygame

pygame.init()


class BaseEntity:
    def __init__(self):
        pass

    def draw(self):
        pass

    def handle_events(self, event):
        pass
