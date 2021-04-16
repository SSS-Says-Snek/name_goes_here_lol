from Engine.States.base_state import BaseState, DummyState
from button import MenuButton
from common import *
from utils import *

from pygame import *


class MenuState(BaseState):
    def __init__(self):
        super().__init__()
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
            ), NotImplemented),
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
                font_size=40
            ), lambda: self.change_state(StatState)),
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
                self.buttons[list(self.buttons.keys())[self.selection]][1]()
        if pygame_event.type == MOUSEBUTTONDOWN:
            self.buttons[list(self.buttons.keys())[self.selection]][1]()

        for dict_key, button in self.buttons.items():
            if button[0].get_rect().collidepoint((mousex, mousey)):
                self.selection = list(self.buttons.keys()).index(dict_key)

    def change_state(self, other_state):
        global CurrentState
        print("Current State", repr(CurrentState))
        print("Other State:", repr(other_state))
        print("Current state doc for handle_events:", CurrentState.handle_events.__doc__)
        print("Current state doc for draw:", CurrentState.draw.__doc__)
        print("Other state doc for handle_events", other_state.handle_events.__doc__)
        print("Other state doc for draw", other_state.draw.__doc__)
        # self.buttons = other_state().buttons
        # CurrentState = other_state
        # temp_draw = other_state().draw
        # temp_handle_events = other_state().handle_events
        CurrentState.draw = other_state().draw
        CurrentState.handle_events = other_state().handle_events
        # other_state().draw = temp_draw
        # other_state().handle_events = temp_handle_events
        print("----------------------TRANSITION-------------------")
        print("Current State", repr(CurrentState))
        print("Other State:", repr(other_state))
        print("Current state doc for handle_events:", CurrentState.handle_events.__doc__)
        print("Current state doc for draw:", CurrentState.draw.__doc__)
        print("Other state doc for handle_events", other_state.handle_events.__doc__)
        print("Other state doc for draw", other_state.draw.__doc__)

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
    def __init__(self):
        super().__init__()
        self.buttons = {"test_button": (MenuButton(self.screen, ((100, 100), (100, 100)), (128, 128, 128), text="Bacc",
                                                   text_color=(0, 0, 0), font_size=40), lambda: self.change_state(MenuState))}

    def draw(self):
        """STATSTATE doc for draw"""
        txt = self.font.render("Statistics Yes", True, (0, 0, 0))
        self.screen.blit(txt, (200, 200))
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
                # self.change_state(MenuState)

    def change_state(self, other_state):
        global CurrentState
        print("CurrentState is identical to other_state:", CurrentState == other_state)
        print("Current State", repr(CurrentState))
        print("Other State:", repr(other_state))
        print("Current state doc for handle_events:", CurrentState.handle_events.__doc__)
        print("Current state doc for draw:", CurrentState.draw.__doc__)
        print("Other state doc for handle_events", other_state.handle_events.__doc__)
        print("Other state doc for draw", other_state.draw.__doc__)
        # CurrentState = other_state
        # temp_draw = other_state().draw
        # temp_handle_events = other_state().handle_events
        CurrentState.draw = other_state().draw
        CurrentState.handle_events = other_state().handle_events
        # other_state().draw = temp_draw
        # other_state().handle_events = temp_handle_events
        print("-----------------TRANSITION-----------------")
        print("CurrentState is identical to other_state:", CurrentState == other_state)
        print("Current State", repr(CurrentState))
        print("Other State:", repr(other_state))
        print("Current state doc for handle_events:", CurrentState.handle_events.__doc__)
        print("Current state doc for draw:", CurrentState.draw.__doc__)
        print("Other state doc for handle_events", other_state.handle_events.__doc__)
        print("Other state doc for draw", other_state.draw.__doc__)


CurrentState = MenuState
