from common import *
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


@lru_cache(1000)
def font(size, text_font="ThaleahFat"):
    return pygame.font.Font(FONT_PATH / f"{text_font}.ttf", size)


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
