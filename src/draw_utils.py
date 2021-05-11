from src.common import *
from src.utils import *


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


def blit_on_center(surface, pos, screen=SCREEN):
    rect_of_surface = surface.get_rect()
    rect_of_surface.center = pos
    screen.blit(surface, rect_of_surface)
