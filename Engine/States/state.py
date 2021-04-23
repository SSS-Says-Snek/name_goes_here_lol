import pygame_gui
from Engine.States.base_state import BaseState, DummyState
from Engine.button import MenuButton
from Engine.other import PopUpMessage
from common import *
from utils import *

from pygame.locals import *


class MenuState(BaseState):
    """State that handles menu things"""

    def __init__(self):
        super().__init__()
        self.next_state = MenuState

        self.selection = 0
        self.title = TITLE
        self.title_idx = 0
        self.title_thing = 0
        self.buttons = {
            "start_button": (MenuButton(
                self.screen,
                ((250, 100), (275, 75)),
                (128, 128, 128),
                text="Start New Game",
                text_color=(0, 0, 0),
                font_size=40
            ), lambda: self.change_state(NewGameState)),
            "load_button": (MenuButton(
                self.screen,
                ((250, 200), (350, 75)),
                (128, 128, 128),
                text="Load Existing Game",
                text_color=(0, 0, 0),
                font_size=40
            ), NotImplemented),
            "stat_button": (MenuButton(
                self.screen,
                ((250, 300), (250, 75)),
                (128, 128, 128),
                text="Statistics",
                text_color=(0, 0, 0),
                font_size=40), lambda: self.change_state(StatState)),
            "quit_button": (MenuButton(
                self.screen,
                ((250, 400), (100, 75)),
                (128, 128, 128),
                text="Quit",
                text_color=(0, 0, 0),
                font_size=40
            ), exit_game)
        }

    def draw(self):
        """MenuState doc for draw"""
        self.update_title()
        for dict_key, button in self.buttons.items():
            # The button is a tuple of two things: the actual button, and the action
            if self.selection == list(self.buttons).index(dict_key):
                button[0].draw((0, 128, 0))
            else:
                button[0].draw()

    def handle_events(self, pygame_event):
        """MenuState doc for handle_events"""
        mousex, mousey = pygame.mouse.get_pos()

        if pygame_event.type == KEYDOWN:
            if pygame_event.key == K_DOWN:
                print('yes')
                self.selection += 1
                self.selection %= len(self.buttons)
            if pygame_event.key == K_UP:
                print('yes yes')
                self.selection -= 1
                self.selection %= len(self.buttons)
            if pygame_event.key == K_RETURN:
                try:
                    self.buttons[list(self.buttons.keys())[self.selection]][1]()
                except TypeError:
                    print("Not Implemented, shh")
        if pygame_event.type == MOUSEBUTTONDOWN:
            for button in self.buttons.values():
                if button[0].get_rect().collidepoint((mousex, mousey)):
                    try:
                        button[1]()
                    except TypeError:
                        print("Not Implemented, shh")

        for dict_key, button in self.buttons.items():
            if button[0].get_rect().collidepoint((mousex, mousey)):
                self.selection = list(self.buttons.keys()).index(dict_key)

    def process_state_event(self, state_event):
        if state_event == 3:
            return StatState
        return self

    def update_title(self):
        for i in self.title:
            if self.title_idx == self.title_thing:
                title_surf = self.font.render(i, True, (0, 255, 0))
            else:
                title_surf = self.font.render(i, True, (0, 128, 0))
            self.screen.blit(title_surf, (WIDTH // 2 - len(self.title) * 13 + self.title_idx * 30, 0))
            self.title_idx += 1
            self.title_idx %= len(self.title)

        self.title_thing += 1
        self.title_thing %= len(self.title)


class StatState(BaseState):
    """State that represents the statistics screen inside the main menu"""

    def __init__(self):
        super().__init__()
        self.next_state = StatState

        self.buttons = {"test_button": (MenuButton(self.screen, ((100, 100), (100, 100)), (128, 128, 128), text="Bacc",
                                                   text_color=(0, 0, 0), font_size=40), lambda: self.change_state(MenuState))}

    def draw(self):
        """STATSTATE doc for draw"""
        txt = self.font.render("Game Statistics", True, (0, 0, 0))
        self.screen.blit(txt, (200, 20))
        for dict_key, button in self.buttons.items():
            button[0].draw()

    def handle_events(self, pygame_event):
        """STATSTATE doc for handle_events"""
        if pygame_event.type == MOUSEBUTTONDOWN:
            print('yes')
            mousex, mousey = pygame.mouse.get_pos()
            if self.buttons["test_button"][0].get_rect().collidepoint((mousex, mousey)):
                self.buttons["test_button"][1]()
                print(MenuState.draw.__doc__)


class NewGameState(BaseState):
    def __init__(self):
        # important things
        super().__init__()
        self.next_state = NewGameState
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT), PATH / "Assets/Themes/test_theme.json")
        self.clock = pygame.time.Clock()
        self.screen_width, self.screen_height = self.screen.get_size()

        # not so important things used in two or more methods
        self.buttons = {"okay_button": (MenuButton(self.screen, ((450, 300), (200, 50)), rect_color=(128, 128, 128),
                                                   text="Okay", text_color=(0, 0, 0), font_size=20), lambda: self.okay()),
                        "cancel_button": (MenuButton(self.screen, ((150, 300), (200, 50)), rect_color=(128, 128, 128),
                                                     text="Cancel", text_color=(0, 0, 0), font_size=20),
                                          lambda: self.change_state(MenuState))}
        self.new_game_input_box = pygame.Rect((100, 300), (500, 200))
        self.new_game_input_box.center = (self.screen_width // 2, self.screen_height // 2)
        self.new_game_input = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=self.new_game_input_box, manager=self.manager
        )
        self.no_text_in_input = False

    def draw(self):
        dt = self.clock.tick(30) / 1000
        new_game_txt = font(51).render("Enter File name for new game:", True, (0, 0, 0))
        new_game_txt_rect = new_game_txt.get_rect(center=(self.screen_width // 2, 40))
        self.screen.blit(new_game_txt, new_game_txt_rect)
        for dict_key, button in self.buttons.items():
            button[0].draw()

        if self.no_text_in_input:
            swidth, sheight = self.screen.get_size()
            popup = PopUpMessage((swidth // 2, sheight // 2, 200, 150), rect_color=(150, 150, 150),
                                 text="Please provide a name for the file!", text_font=font(30), screen=self.screen)
            popup.draw()

        self.manager.update(dt)
        self.manager.draw_ui(self.screen)

        pygame.display.update()

    def handle_events(self, event):
        mousex, mousey = pygame.mouse.get_pos()
        self.new_game_input.enable()
        self.new_game_input.focus()
        self.new_game_input.rebuild_from_changed_theme_data()
        self.new_game_input.process_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for key, button in self.buttons.items():
                if button[0].get_rect().collidepoint((mousex, mousey)):
                    button[1]()

    def okay(self):
        input_text = self.new_game_input.get_text()
        if input_text != '':
            print("Ye")
            print(f"Ze text you typed is: {input_text}")
        else:
            print("Nuu")
            swidth, sheight = self.screen.get_size()
            # popup = PopUpMessage((swidth // 2, sheight // 2, 200, 150), rect_color=(150, 150, 150),
            #                      text="Please provide a name for the file!", text_font=font(30), screen=self.screen)
            # popup.draw()
            self.no_text_in_input = True
        # self.change_state(MenuState)
