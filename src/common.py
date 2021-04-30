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
