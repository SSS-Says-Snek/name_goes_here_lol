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


def blit_multicolor_text(text_font, text_list: dict, coord_to_blit, screen=SCREEN):
    """
    Function used to render multicolored text. Used as:
    >>> blit_multicolor_text(font(20), {"Text lol": (128, 128, 128), "More Text": (128, 0, 0)})
    <blits font rendering with "Text lol" colored gray, and "More Text" colored red>
    """
    actual_coord_to_blit = coord_to_blit
    for key, value in text_list.items():
        text_font_part = text_font.render(key, True, value)
        screen.blit(text_font_part, actual_coord_to_blit)
        actual_coord_to_blit = (actual_coord_to_blit[0] + text_font.size(key)[0], actual_coord_to_blit[1])


def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotated_image, new_rect


def is_hovering(rect, mouse_pos):
    if rect.left <= mouse_pos[0] <= rect.right and rect.top <= mouse_pos[1] <= rect.bottom:
        return True
    return False


def exit_game():
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
    return pygame.image.load(IMG_PATH / image_name)


@lru_cache(1000)
def font(size, text_font="ThaleahFat"):
    return pygame.font.Font(FONT_PATH / f"{text_font}.ttf", size)
