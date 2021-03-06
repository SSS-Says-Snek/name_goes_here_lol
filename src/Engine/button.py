import functools

from src import common
from src import utils

import pygame
from typing import Union

pygame.init()
pygame.font.init()


class Button:
    """
    Coordinates can be in the form of ((top left x, top left y), (width, height)) or
    (top left x, top left y, width, height)
    Creates a button on a given screen, with coordinates similar to pygame.Rect().
    Text is optional for the button, and rounding corners is supported
    """

    def __init__(
        self,
        surface,
        coordinates: tuple,
        rect_color=(255, 255, 255),
        text=None,
        text_color=(0, 0, 0),
        font_size=None,
        rounded=True,
        func_when_clicked=None,
    ):
        self.screen = surface
        self.coords = coordinates
        self.rect_color = rect_color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.rounded = rounded
        self.func_when_clicked = func_when_clicked

    def draw(self, rect_color=None):
        rect = pygame.Rect(self.coords)
        pygame.draw.rect(
            self.screen, self.rect_color, rect, border_radius=20 if self.rounded else 0
        )
        if self.text:
            if self.font_size is None:
                # Doesn't work but ok
                self.font_size = (
                    self.coords[3] // len(self.text)
                    if len(self.coords) == 4
                    else self.coords[1][0] // len(self.text)
                )
            font_different_size = pygame.font.Font(
                common.PATH / "Assets/Fonts/ThaLeahFat.ttf", self.font_size
            )
            text_surf = font_different_size.render(self.text, True, self.text_color)
            self.screen.blit(
                text_surf,
                (
                    rect.centerx - text_surf.get_width() // 2,
                    rect.centery - text_surf.get_height() // 2,
                ),
            )

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.func_when_clicked()

    def get_rect(self):
        return pygame.Rect(self.coords)


class ImageButton:
    """An Image button used a bit like the Button and MenuButton class"""

    def __init__(self, surface, image_name, coord_to_blit, scale=None, resize_to=None):
        self.surface = surface
        self.image = utils.load_image(image_name)
        self.coord_to_blit = coord_to_blit
        self.scale = scale
        self.resize_to = resize_to

        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = coord_to_blit

        if self.scale is not None:
            self.image = pygame.transform.smoothscale(
                self.image,
                (
                    self.image.get_size()[0] * self.scale,
                    self.image.get_size()[1] * self.scale,
                ),
            )
        elif self.resize_to is not None:
            self.image = pygame.transform.smoothscale(self.image, self.resize_to)

        self.image.convert()

    def draw(self):
        self.surface.blit(self.image, self.coord_to_blit)

    @functools.lru_cache(1000)
    def get_rect(self):
        return self.image_rect


class MenuButton(Button):
    """Subset of Button, MenuButton adds features suitable for Menu Buttons"""

    def __init__(
        self,
        surface,
        coordinates: tuple,
        rect_color=(255, 255, 255),
        text=None,
        text_color=(0, 0, 0),
        font_size=None,
        rounded=False,
    ):
        super().__init__(
            surface, coordinates, rect_color, text, text_color, font_size, rounded
        )

    def draw(self, rect_color=None):
        """Draws the button onto previously inputted screen"""
        rect = pygame.Rect(self.coords)
        if rect_color is None:
            pygame.draw.rect(
                self.screen,
                self.rect_color,
                rect,
                border_radius=20 if self.rounded else 0,
                width=2,
            )
        else:
            # pygame.draw.rect(self.screen, self.rect_color, rect, border_radius=20 if self.rounded else 0, width=2)
            smaller_rect = pygame.Rect(
                self.coords[0][0] + 2,
                self.coords[0][1] + 2,
                self.coords[1][0] - 2,
                self.coords[1][1] - 2,
            )
            pygame.draw.rect(
                self.screen,
                self.rect_color,
                rect,
                border_radius=20 if self.rounded else 0,
                width=2,
            )
            pygame.draw.rect(self.screen, rect_color, smaller_rect)
        if self.text:
            if self.font_size is None:
                # Doesn't work but ok
                self.font_size = (
                    self.coords[3] // len(self.text)
                    if len(self.coords) == 4
                    else self.coords[1][0] // len(self.text)
                )
            font_different_size = pygame.font.Font(
                common.PATH / "src/Assets/Fonts/ThaleahFat.ttf", self.font_size
            )
            text_surf = font_different_size.render(self.text, True, self.text_color)
            self.screen.blit(
                text_surf,
                (
                    rect.centerx - text_surf.get_width() // 2,
                    rect.centery - text_surf.get_height() // 2,
                ),
            )


class RadioButton:
    def __init__(self, buttons):
        """I'm lazy, I'll do it someday"""
        pass


class ToggleButton:
    def __init__(
        self,
        default="off",
        off_color=(255, 0, 0),
        on_color=(0, 255, 0),
        screen=common.SCREEN,
    ):
        self.default = default
        self.off_color = off_color
        self.on_color = on_color
        self.screen = screen


class HiddenButton:
    """Definately did not copy paste this from my old project"""

    def __init__(
        self, access, name, image_filename: Union[str, pygame.Rect], location, size
    ):
        self.access = access
        self.name = name
        self.image = pygame.image.load(f"images/{image_filename}")
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.x = location[0]
        self.rect.y = location[1]
