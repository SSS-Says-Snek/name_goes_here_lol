import pygame
from pathlib import Path

pygame.init()
pygame.font.init()

PATH = Path(".")
WIDTH, HEIGHT = (800, 600)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
TITLE = "Name Goes Here Lol"
