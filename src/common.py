"""
Some common variables used many times throughout the game code
=============================  U S A G E  =============================
>>> from src.common import *
>>> # Use the variables here
"""
__version__ = "-4.4.5.b-1"

import pygame
from pathlib import Path

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = (800, 600)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
TITLE = "Name Goes Here Lol"

PATH = Path(".")
FONT_PATH = PATH / "src/Assets/Fonts"
IMG_PATH = PATH / "src/Assets/Images"
DATA_PATH = PATH / "src/Assets/Data"
