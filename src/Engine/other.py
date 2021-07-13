"""
Other random classes that I might use for other stuff
"""

import random

from src.Engine.button import MenuButton
from src.utils import *

import pygame
from pygame.locals import *


class TextBox:
    def __init__(
        self,
        coordinates,
        beginning_text="",
        inactive_color=pygame.Color("lightskyblue3"),
        active_color=pygame.Color("dodgerblue2"),
        fontsize=60,
    ):
        self.rect = pygame.Rect(coordinates)
        self.text = beginning_text
        self.color = inactive_color
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.active = False
        self.fontsize = fontsize

        self.font = font(self.fontsize)
        self.txt_surface = self.font.render(self.text, True, self.color)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self if self.active_color else self.inactive_color
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class DropDown:
    def __init__(
        self, screen, color_menu, color_option, coords, dropdown_font, main, options
    ):
        self.screen = screen
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pygame.Rect(coords)
        self.font = dropdown_font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self):
        pygame.draw.rect(self.screen, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        self.screen.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(
                    self.screen,
                    self.color_option[1 if i == self.active_option else 0],
                    rect,
                    0,
                )
                msg = self.font.render(text, 1, (0, 0, 0))
                self.screen.blit(msg, msg.get_rect(center=rect.center))

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
        return -1


class Menu:
    """Scrapped version of Menu, but might need it someday..."""

    def __init__(self, surface):
        self.font = pygame.font.Font(PATH / "Assets/Fonts/ThaleahFat.ttf", 60)
        self.screen = surface
        self.title = TITLE
        self.title_idx = 0
        self.menustate = "main menu"
        self.selection = 0  # 0th index
        self.buttons = {
            "start_button": MenuButton(
                self.screen,
                ((250, 100), (275, 75)),
                (128, 128, 128),
                text="Start New Game",
                text_color=(0, 0, 0),
                font_size=40,
            ),
            "load_button": MenuButton(
                self.screen,
                ((250, 200), (200, 75)),
                (128, 128, 128),
                text="Load Game",
                text_color=(0, 0, 0),
                font_size=40,
            ),
            # "home_button": MenuButton(
            #     self.screen,
            #     ((0, 0), (75, 75)),
            #     (255, 0, 0),
            #     text_color=(0, 0, 0),
            #     font_size=40,
            #     rounded=False
            # ),
            # "another_text_button": MenuButton(
            #     self.screen,
            #     ((400, 400), (75, 75)),
            #     (0, 255, 0),
            #     text="Text",
            #     text_color=(0, 0, 0),
            #     font_size=40,
            #     rounded=False
            # )
        }
        self.something_test = 0
        self.angle_to_rotate = 0
        self.amount_to_rotate_by = 2
        self.rand_font = random.randint(50, 250)
        self.rand_pos = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

    def draw(self):
        self.update_title()
        self.generate_dollar_sign(self.rand_font, self.rand_pos, (0, 255, 0))

        for key, button in self.buttons.items():
            if self.menustate == "main menu":
                button.draw()

    def handle_events(self):
        for events in pygame.events.get():
            if events.type == KEYDOWN:
                if events.key == K_DOWN:
                    self.selection += 1
                    self.selection %= len(self.buttons)

    def update_title(self):
        for i in self.title:
            # random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if self.title_idx == self.something_test:
                title_surf = self.font.render(i, True, (0, 255, 0))
            else:
                title_surf = self.font.render(i, True, (0, 128, 0))
            self.screen.blit(
                title_surf, (WIDTH // 2 - len(self.title) * 13 + self.title_idx * 30, 0)
            )
            self.title_idx += 1
            self.title_idx %= len(self.title)

        self.something_test += 1
        self.something_test %= len(self.title)

    def generate_dollar_sign(self, size, pos, color=(0, 255, 0)):
        dollar_sign = font(size).render("$", True, color)
        dollar_sign = rot_center(dollar_sign, self.angle_to_rotate, pos[0], pos[1])
        self.screen.blit(dollar_sign[0], dollar_sign[1])
        self.angle_to_rotate -= self.amount_to_rotate_by
        if self.angle_to_rotate <= -30:
            self.amount_to_rotate_by = -2
        if self.angle_to_rotate >= 10:
            self.amount_to_rotate_by = 2


class PopUpMessage:
    def __init__(
        self,
        coords: tuple,
        rect_color=(0, 0, 0),
        text=None,
        text_font=None,
        screen=SCREEN,
    ):
        self.screen = screen
        self.coords = coords
        self.rect_color = rect_color
        self.text = text
        self.text_font = text_font
        self.running = True

    def draw(self):
        messagebox_rect = pygame.Rect(self.coords)
        pygame.draw.rect(self.screen, self.rect_color, messagebox_rect)
        if self.text is not None and self.text_font is not None:
            text_words = self.text.split(" ")
            lines = []
            # Let's just assume for now that it's tuple[int, int, int, int] for big brain time
            while len(text_words) > 0:
                word_lines = []
                while len(text_words) > 0:
                    word_lines.append(text_words.pop(0))
                    font_width, font_height = self.text_font.size(
                        " ".join(word_lines + text_words[:1])
                    )
                    print(word_lines + text_words[:1])
                    if font_width > self.coords[3]:
                        break
                line = " ".join(word_lines)
                lines.append(line)
            print(lines)
            y_offset = 0
            for line in lines:
                font_width, font_height = self.text_font.size(line)
                top_left_x = self.coords[0]
                top_left_y = self.coords[1] + y_offset
                font_surface = self.text_font.render(line, True, (0, 0, 0))
                self.screen.blit(font_surface, (top_left_x, top_left_y))

                y_offset += font_height

    def stop_running(self):
        self.running = False


class OkayPopUpMessage(PopUpMessage):
    def __init__(
        self,
        coords: tuple,
        rect_color=(0, 0, 0),
        text=None,
        text_font=None,
        screen=SCREEN,
    ):
        super().__init__(coords, rect_color, text, text_font, screen)


class Slider:
    def __init__(
        self,
        coord,
        color,
        length,
        width,
        min_val,
        max_val,
        default_val=None,
        screen=SCREEN,
        num_spaces=-1,
        slide_color=None,
        show_value=True,
    ):
        self.coord = coord
        self.color = color
        self.length = length
        self.width = width
        self.min_val = min_val
        self.max_val = max_val
        self.screen = screen
        self.num_spaces = num_spaces
        self.show_value = show_value

        if default_val is None:
            self.default_val = self.min_val
        else:
            self.default_val = default_val

        if slide_color is None:
            self.slide_color = self.color
        else:
            self.slide_color = slide_color
        self.rect_coord = self.coord + (
            self.length,
            self.width,
        )
        self.rect = pygame.Rect(self.rect_coord)
        self.font = font(self.width)
        self.is_holding_mouse = False
        self.slide_coord = (
            self.coord[0]
            + (self.default_val - self.min_val) / self.max_val * self.length,
            self.coord[1] - width // 2,
        )
        self.current_val = self.default_val

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(self.screen, self.color, self.rect_coord)
        min_val_txt = self.font.render(str(self.min_val), True, (0, 0, 0))
        min_val_txt_rect = min_val_txt.get_rect(
            topright=(self.coord[0] - (self.length // 30), self.coord[1])
        )
        self.screen.blit(min_val_txt, min_val_txt_rect)

        max_val_txt = self.font.render(str(self.max_val), True, (0, 0, 0))
        self.screen.blit(
            max_val_txt,
            (self.coord[0] + self.length + self.length // 30, self.coord[1]),
        )

        current_rect = pygame.draw.rect(
            self.screen, self.slide_color, self.slide_coord + (20, self.width * 2)
        )
        if self.show_value:
            current_val_txt = self.font.render(str(self.current_val), True, (0, 0, 0))
            current_val_txt_rect = current_val_txt.get_rect(
                center=(current_rect.midbottom[0], current_rect.centery - self.width)
            )
            self.screen.blit(current_val_txt, current_val_txt_rect)
        if (
            self.is_holding_mouse
            and self.coord[0] <= mouse_pos[0] <= self.coord[0] + self.length
        ):
            # if self.is_holding_mouse and distance(mouse_pos[0], current_rect.centerx, mouse_pos[1], current_rect.centery) < 100:
            self.slide_coord = (mouse_pos[0], self.slide_coord[1])
            self.current_val = (
                mouse_pos[0] - self.coord[0]
            ) / self.length * self.max_val + self.default_val
            if self.current_val > self.max_val:
                self.current_val = self.max_val
            self.current_val = round(self.current_val)

    def handle_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(mouse_pos):
            self.is_holding_mouse = True
        if event.type == MOUSEBUTTONUP:
            self.is_holding_mouse = False

    def get_slide_value(self):
        return self.current_val


class GameData:
    def __init__(self):
        self.camera_offset = [0, 0]
        self.game_fps = load_setting("fps")


class GameException(Exception):
    """Just the default game exception"""

    pass


game_data = GameData()
