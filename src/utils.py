import json

from src.common import *
from functools import lru_cache

import sys
import pygame

pygame.init()
pygame.font.init()


def extract_items_from_list(list_thing):
    for item in list_thing:
        if isinstance(item, list):
            yield from extract_items_from_list(item)
        else:
            yield item


def rot_center(image, angle, x, y):
    """Rotates an image based on its center to avoid different """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotated_image, new_rect


def is_hovering(rect, mouse_pos):
    """Checks if a mouse is hovering over a rect"""
    if rect.left <= mouse_pos[0] <= rect.right and rect.top <= mouse_pos[1] <= rect.bottom:
        return True
    return False


def exit_game():
    """Exits the game with pygame.quit() and sys.exit()"""
    pygame.quit()
    sys.exit(0)


def format_byte(size: int, decimal_places=3):
    """Formats a given size and outputs a string equivalent to B, KB, MB, GB, or TB"""
    if size < 1e03:
        return f"{round(size, decimal_places)} B"
    if size < 1e06:
        return f"{round(size / 1e3, decimal_places)} KB"
    if size < 1e09:
        return f"{round(size / 1e6, decimal_places)} MB"
    if size < 1e12:
        return f"{round(size / 1e9, decimal_places)} GB"
    return f"{round(size / 1e12, decimal_places)} TB"


@lru_cache()
def load_image(image_name):
    """Loads an image from the asset folder"""
    return pygame.image.load(IMG_PATH / image_name)


@lru_cache(1000)
def font(size, text_font="ThaleahFat"):
    """Loads a font with a given size and an optional parameter for the font name"""
    return pygame.font.Font(FONT_PATH / f"{text_font}.ttf", size)


def load_setting(key_to_load):
    with open(DATA_PATH / "config.json") as read_setting_file:
        all_settings_info = json.load(read_setting_file)
    try:
        return all_settings_info[key_to_load]
    except KeyError:
        return None
