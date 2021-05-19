import pygame_gui
from src.Engine.States.base_state import BaseState
from src.Engine.States.pause import PauseMenu
from src.Engine.button import *
from src.Engine.other import Slider
from src.utils import *
from src.draw_utils import *

from pygame.locals import *


class MenuState(BaseState):
    """State that handles menu things"""

    def __init__(self):
        super().__init__()

        self.selection = 0
        self.title = TITLE
        self.title_idx = 0
        self.title_thing = 0
        self.TITLEUPDATE = pygame.USEREVENT + 1
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
            "setting_button": (MenuButton(
                self.screen,
                ((250, 400), (225, 75)),
                (128, 128, 128),
                text="Settings",
                text_color=(0, 0, 0),
                font_size=40), lambda: self.change_state(SettingState)
            ),
            "quit_button": (MenuButton(
                self.screen,
                ((250, 500), (100, 75)),
                (128, 128, 128),
                text="Quit",
                text_color=(0, 0, 0),
                font_size=40
            ), lambda: exit_game())
        }

        pygame.time.set_timer(self.TITLEUPDATE, 33)

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
                print('Menu Selection Down')
                self.selection += 1
                self.selection %= len(self.buttons)
            if pygame_event.key == K_UP:
                print('Menu Selection Up')
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
        if pygame_event.type == self.TITLEUPDATE:
            self.title_thing += 1
            self.title_thing %= len(self.title)

        for dict_key, button in self.buttons.items():
            if button[0].get_rect().collidepoint((mousex, mousey)):
                self.selection = list(self.buttons.keys()).index(dict_key)

    def process_state_event(self, state_event):
        if state_event == 3:
            return StatState
        return self

    def update_title(self):
        blit_multicolor_text(
            self.font, {
                self.title[:self.title_thing]: (0, 128, 0),
                self.title[self.title_thing]: (0, 255, 0),
                self.title[self.title_thing + 1:]: (0, 128, 0)
            }, (
                160, 0
            )
        )


class StatState(BaseState):
    """State that represents the statistics screen inside the main menu"""

    def __init__(self):
        super().__init__()

        self.buttons = {
            "test_button": (
                MenuButton(self.screen, ((100, 100), (100, 100)), (128, 128, 128), text="Home",
                           text_color=(0, 0, 0), font_size=40),
                lambda: self.change_state(MenuState)
            )
        }

    def draw(self):
        """STATSTATE doc for draw"""
        txt = self.font.render("Game Statistics", True, (0, 0, 0))
        self.screen.blit(txt, (200, 20))
        for dict_key, button in self.buttons.items():
            button[0].draw()

    def handle_events(self, pygame_event):
        """STATSTATE doc for handle_events"""
        if pygame_event.type == MOUSEBUTTONDOWN:
            mousex, mousey = pygame.mouse.get_pos()
            for name, button in self.buttons.items():
                if button[0].get_rect().collidepoint((mousex, mousey)):
                    button[1]()


class SettingState(BaseState):
    """State that represents the setting screen inside the main menu"""

    def __init__(self):
        super().__init__()

        self.buttons = {
            (
                MenuButton(self.screen, ((70, 50), (100, 100)), (128, 128, 128), text="Back",
                           text_color=(0, 0, 0), font_size=40),
                lambda: self.change_state(MenuState)
            ),
            (
                MenuButton(self.screen, ((600, 490), (150, 100)), (128, 128, 128), text="Okay",
                           text_color=(0, 0, 0), font_size=40),
                lambda: self.change_state(MenuState)
            ),
            (
                MenuButton(self.screen, ((400, 490), (150, 100)), (128, 128, 128), text="Apply",
                           text_color=(0, 0, 0), font_size=40),
                lambda: self.apply_changes()
            )
        }
        self.fps_slider = Slider((200, 200), (230, 230, 0), 500, 40, 10, 500, slide_color=(0, 128, 0))

    def draw(self):
        txt = self.font.render("Game Settings", True, (0, 0, 0))
        blit_on_center(txt, (400, 30))

        self.fps_slider.draw()
        for button in self.buttons:  # .items():
            button[0].draw()

    def handle_events(self, pygame_event):
        self.fps_slider.handle_events(pygame_event)
        if pygame_event.type == MOUSEBUTTONDOWN:
            mousex, mousey = pygame.mouse.get_pos()
            for button in self.buttons:  # .items():
                if button[0].get_rect().collidepoint((mousex, mousey)):
                    button[1]()

    def apply_changes(self):
        """
        Right now, you need to restart game for it to take change, hang on, I'm gonna change that soon-ish (TM)
        """
        fps = self.fps_slider.get_slide_value()

        modify_setting("fps", fps)
        print(fps)


class NewGameState(BaseState):
    """State that handles the "new game" file making"""

    def __init__(self):
        # important things
        super().__init__()
        # self.next_state = NewGameState
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT), PATH / "src/Assets/Themes/test_theme.json")
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

    def draw(self):
        dt = self.clock.tick(30) / 1000
        new_game_txt = font(51).render("Enter File name for new game:", True, (0, 0, 0))
        new_game_txt_rect = new_game_txt.get_rect(center=(self.screen_width // 2, 40))
        self.screen.blit(new_game_txt, new_game_txt_rect)
        for dict_key, button in self.buttons.items():
            button[0].draw()

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
            print(f"Ze text you typed is: {input_text}\nRedirecting to game screen...")
            self.change_state(PlayingGameState)
        else:
            print("No Text Selected, to be implemented (Or use placeholder text)\nRedirecting to main menu...")
            self.change_state(MenuState)


class PlayingGameState(BaseState):
    """IMPORTANT: This state actually allows you to play the game, controlling your player (a snake)"""

    def __init__(self):
        super().__init__()

        self.buttons = {
            "pause_button": ([ImageButton(self.screen, "pause.png", (700, 0)),
                              ImageButton(self.screen, "play.png", (700, 0))], NotImplemented)
        }
        self.pause_menu = PauseMenu()
        self.background = load_image("bg.png").convert()

    def draw(self):
        play_game_txt = font(40).render("Lorem ipsum", True, (0, 0, 0))
        self.screen.blit(play_game_txt, (300, 0))
        self.screen.blit(self.background, (0, 0))
        self.pause_menu.draw()

        for button in self.buttons.values():
            if self.pause_menu.draw_pause:
                button[0][1].draw()
            else:
                button[0][0].draw()

    def handle_events(self, event):
        mousex, mousey = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN:
            for button_name, button in self.buttons.items():
                if self.pause_menu.draw_pause:
                    if button[0][1].get_rect().collidepoint((mousex, mousey)):
                        self.pause_menu.toggle_menu()
                else:
                    if button[0][0].get_rect().collidepoint((mousex, mousey)):
                        self.pause_menu.toggle_menu()
        self.pause_menu.handle_events(event)
