"""
Other random classes that I might use for other stuff
"""

from src import utils
from src import common

import pygame


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

        self.font = utils.load_font(self.fontsize)
        self.txt_surface = self.font.render(self.text, True, self.color)

    def handle_events(self, event):
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


class PopUpMessage:
    def __init__(
        self,
        coords: tuple,
        rect_color=(0, 0, 0),
        text=None,
        text_font=None,
        screen=common.SCREEN,
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
        screen=common.SCREEN,
    ):
        super().__init__(coords, rect_color, text, text_font, screen)


class Slider:
    # pylint: disable=too-many-instance-attributes
    # Well, whaddya expect, there needs to be a lot to customize the slider

    def __init__(
        self,
        coord,
        color,
        length,
        width,
        min_val,
        max_val,
        default_val=None,
        screen=common.SCREEN,
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
        self.font = utils.load_font(self.width)
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
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse_pos):
            self.is_holding_mouse = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.is_holding_mouse = False

    def get_slide_value(self):
        return self.current_val


class TextMessage:
    def __init__(
        self,
        pos,
        width,
        height,
        rect_color,
        text,
        font,
        font_color=(0, 0, 0),
        border_color=None,
        border_width=None,
        instant_blit=True,
        screen=common.SCREEN,
    ):
        """This class can be used to display text"""
        self.pos = pos
        self.width = width
        self.height = height
        self.rect_color = rect_color
        self.text = text
        self.font = font
        self.font_color = font_color
        self.border_color = border_color
        self.border_width = border_width
        self.instant_blit = instant_blit
        self.screen = screen

        self.text_rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.split_text = utils.wrap_text(
            self.text, self.width - (self.border_width or 0), self.font
        )

        if not self.instant_blit:
            self.blitted_chars = ["" for _ in self.split_text]
            self.char_blit_line = 0
            self.blit_line_idx = 0
            self.prev_line_text = ""

    def draw(self):
        pygame.draw.rect(self.screen, self.rect_color, self.text_rect)

        if self.border_color is not None and self.border_width is not None:
            pygame.draw.rect(
                self.screen, self.border_color, self.text_rect, width=self.border_width
            )

        if self.instant_blit:
            for i, text in enumerate(self.split_text):
                rendered_text = self.font.render(text, True, self.font_color)
                self.screen.blit(
                    rendered_text,
                    (
                        self.pos[0] + (self.border_width or 0),
                        self.pos[1] + i * self.font.get_height(),
                    ),
                )

        else:
            self.char_blit_line += 1

            prev_text = self.split_text[self.blit_line_idx][: self.char_blit_line]
            self.blitted_chars[self.blit_line_idx] = self.split_text[
                self.blit_line_idx
            ][: self.char_blit_line]

            if self.blitted_chars[self.blit_line_idx] == self.prev_line_text:
                if self.blit_line_idx + 1 < len(self.split_text):
                    self.char_blit_line = 0
                    self.blit_line_idx += 1

            for i, text in enumerate(self.blitted_chars):
                rendered_text = self.font.render(text, True, self.font_color)
                self.screen.blit(
                    rendered_text,
                    (
                        self.pos[0] + (self.border_width or 0),
                        self.pos[1] + i * self.font.get_height(),
                    ),
                )

            self.prev_line_text = prev_text

    def handle_events(self, event):
        if (
            event.type == pygame.KEYDOWN
            and not self.instant_blit
            and self.blitted_chars != self.split_text
        ):
            self.blitted_chars = self.split_text[:]
            self.blit_line_idx = len(self.blitted_chars) - 1
            self.char_blit_line = len(self.blitted_chars[-1])

    def reset_current_text(self):
        """Only applies for non-instant blit textboxes"""
        self.blitted_chars = ["" for _ in self.split_text]
        self.char_blit_line = 0
        self.blit_line_idx = 0
        self.prev_line_text = ""

    @property
    def is_finished(self):
        if not self.instant_blit and self.blitted_chars != self.split_text:
            print("bruv")
            return False
        return True


class GameData:
    def __init__(self):
        """Contains information about the game"""
        self.camera_offset = [0, 0]
        self.game_fps = utils.load_setting("fps")
        self.player = None  # Will be initialized later, in state.py
        self.player_list = {}
        self.current_substate = None
        self.playing_substate = None
        self.player_money = 0


class GameException(Exception):
    """Just the default game exception"""

    pass


game_data = GameData()
