"""
This file contains all state machines used in the game.
Basically, state machines allow us to easily transition from "state" to "state", like from
    a Main Menu to a Settings state
This is mainly used in game.py, though of course, there are exceptions
    (E.g wanting to access a state attribute in a different file)
The basic structure of state machines is:
    - XState.draw()
    - XState.handle_events(event) (Don't ask why it's with an s
    - XState.constant_run() (Optional, but highly recommended)

=============================  U S A G E  =============================
>>> from src.Engine.States.state import MenuState
>>> MenuState().draw()
"""

# Imports
import pygame_gui
import pygame

from src import draw_utils
from src import utils
from src import common
from src.Engine.Entities.player import Player
from src.Engine.Entities.Mobs.enemy import HomingBulletEnemy
from src.Engine.Entities.shop import ShopEntity
from src.Engine.base import BaseState
from src.Engine.objects import Slider, game_data
from src.Engine.button import MenuButton, ImageButton


class MenuState(BaseState):
    """State that handles menu things"""

    def __init__(self, game_class):
        super().__init__(game_class)

        self.selection = 0
        self.title = common.TITLE
        self.title_idx = 0
        self.title_thing = 0
        self.TITLEUPDATE = pygame.USEREVENT + 1

        # List of all buttons, stored as a key-value pair, where
        # key is the name of the button, and value is a tuple with
        # first element as a Button class, and second element as
        # function to call once clicked
        self.buttons = {
            "start_button": (
                MenuButton(
                    self.screen,
                    ((250, 100), (275, 75)),
                    (128, 128, 128),
                    text="Start New Game",
                    text_color=(0, 0, 0),
                    font_size=40,
                ),
                lambda: self.change_state(NewGameState),
            ),
            "load_button": (
                MenuButton(
                    self.screen,
                    ((250, 200), (350, 75)),
                    (128, 128, 128),
                    text="Load Existing Game",
                    text_color=(0, 0, 0),
                    font_size=40,
                ),
                NotImplemented,
            ),
            "stat_button": (
                MenuButton(
                    self.screen,
                    ((250, 300), (250, 75)),
                    (128, 128, 128),
                    text="Statistics",
                    text_color=(0, 0, 0),
                    font_size=40,
                ),
                lambda: self.change_state(StatState),
            ),
            "setting_button": (
                MenuButton(
                    self.screen,
                    ((250, 400), (225, 75)),
                    (128, 128, 128),
                    text="Settings",
                    text_color=(0, 0, 0),
                    font_size=40,
                ),
                lambda: self.change_state(SettingState),
            ),
            "quit_button": (
                MenuButton(
                    self.screen,
                    ((250, 500), (100, 75)),
                    (128, 128, 128),
                    text="Quit",
                    text_color=(0, 0, 0),
                    font_size=40,
                ),
                lambda: utils.exit_game(),
            ),
        }

        pygame.time.set_timer(self.TITLEUPDATE, 33)

    def draw(self):
        """Performs all drawing related tasks related to the Main Menu."""

        # Draws the version at the bottom right
        version_txt = utils.font(15, "PixelMillenium").render(
            f"Version {common.__version__}", True, (0, 0, 0)
        )
        version_txt_rect = version_txt.get_rect(
            bottomright=(common.WIDTH, common.HEIGHT)
        )

        self.screen.blit(version_txt, version_txt_rect)

        # Updates the title
        self.update_title()

        # Loops through all buttons
        for dict_key, button in self.buttons.items():
            # The button is a tuple of two things: the actual button, and the action
            if self.selection == list(self.buttons).index(dict_key):
                button[0].draw((0, 128, 0))
            else:
                button[0].draw()

    def handle_events(self, pygame_event):
        """Handles all events regarding the Main Menu."""
        mousex, mousey = pygame.mouse.get_pos()

        if pygame_event.type == pygame.KEYDOWN:
            if pygame_event.key == pygame.K_DOWN:
                self.selection += 1
                self.selection %= len(self.buttons)
            if pygame_event.key == pygame.K_UP:
                self.selection -= 1
                self.selection %= len(self.buttons)
            if pygame_event.key == pygame.K_RETURN:
                try:
                    self.buttons[list(self.buttons.keys())[self.selection]][1]()
                except TypeError:
                    print("Not Implemented, shh")
        if pygame_event.type == pygame.MOUSEBUTTONDOWN:
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

    def update_title(self):
        """Updates the main menu title."""
        draw_utils.blit_multicolor_text(
            self.font,
            {
                self.title[: self.title_thing]: (0, 128, 0),
                self.title[self.title_thing]: (0, 255, 0),
                self.title[self.title_thing + 1 :]: (0, 128, 0),
            },
            (160, 0),
        )


class StatState(BaseState):
    """State that represents the statistics screen inside the main menu"""

    def __init__(self, game_class):
        super().__init__(game_class)

        # Initializes buttons, like MenuState
        self.buttons = {
            "test_button": (
                MenuButton(
                    self.screen,
                    ((100, 100), (100, 100)),
                    (128, 128, 128),
                    text="Home",
                    text_color=(0, 0, 0),
                    font_size=40,
                ),
                lambda: self.change_state(MenuState),
            )
        }

    def draw(self):
        """Performs all tasks related to drawing related to the Statistics Menu."""
        txt = self.font.render("Game Statistics", True, (0, 0, 0))
        self.screen.blit(txt, (200, 20))
        for dict_key, button in self.buttons.items():
            button[0].draw()

    def handle_events(self, pygame_event):
        """Handles all events related to thte Statistics Menu."""
        if pygame_event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = pygame.mouse.get_pos()
            for name, button in self.buttons.items():
                if button[0].get_rect().collidepoint((mousex, mousey)):
                    button[1]()


class SettingState(BaseState):
    """State that represents the setting screen inside the main menu"""

    def __init__(self, game_class):
        super().__init__(game_class)

        # Initializes the buttons, like in MenuState
        self.buttons = {
            (
                MenuButton(
                    self.screen,
                    ((600, 490), (150, 100)),
                    (128, 128, 128),
                    text="Okay",
                    text_color=(0, 0, 0),
                    font_size=40,
                ),
                lambda: self.change_state(MenuState),
            ),
            (
                MenuButton(
                    self.screen,
                    ((400, 490), (150, 100)),
                    (128, 128, 128),
                    text="Apply",
                    text_color=(0, 0, 0),
                    font_size=40,
                ),
                lambda: self.apply_changes(),
            ),
        }

        # Sets the FPS slider (ranging from 10 to 500)
        self.fps_slider = Slider(
            (200, 100), (230, 230, 0), 500, 40, 10, 500, slide_color=(200, 0, 0)
        )

    def draw(self):
        """Performs all tasks related to drawing related to the Settings Menu."""

        # Blits "Game Settings"
        txt = self.font.render("Game Settings", True, (0, 0, 0))
        draw_utils.blit_on_center(txt, (400, 30))

        fps_txt = utils.font(50).render("FPS:", True, (0, 0, 0))
        self.screen.blit(fps_txt, (40, 100))

        self.fps_slider.draw()

        # Draws all buttons
        for button in self.buttons:
            button[0].draw()

    def handle_events(self, pygame_event):
        """Handles all events related to thte Settings Menu."""

        # Handles FPS Slider events
        self.fps_slider.handle_events(pygame_event)

        # Handles mouse and button events
        if pygame_event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = pygame.mouse.get_pos()
            for button in self.buttons:
                if button[0].get_rect().collidepoint((mousex, mousey)):
                    button[1]()

    def apply_changes(self):
        """Applies the FPS change to the game."""
        fps = self.fps_slider.get_slide_value()

        self.game_class.fps_setting = fps
        game_data.game_fps = fps

        utils.modify_setting("fps", fps)
        print(fps)


class NewGameState(BaseState):
    """State that handles the "new game" file making"""

    def __init__(self, game_class):
        super().__init__(game_class)
        self.manager = pygame_gui.UIManager(
            (common.WIDTH, common.HEIGHT),
            common.PATH / "src/Assets/Themes/test_theme.json",
        )
        self.clock = pygame.time.Clock()
        self.screen_width, self.screen_height = self.screen.get_size()

        # not so important things used in two or more methods
        self.buttons = {
            "okay_button": (
                MenuButton(
                    self.screen,
                    ((450, 300), (200, 50)),
                    rect_color=(128, 128, 128),
                    text="Okay",
                    text_color=(0, 0, 0),
                    font_size=20,
                ),
                lambda: self.okay(),
            ),
            "cancel_button": (
                MenuButton(
                    self.screen,
                    ((150, 300), (200, 50)),
                    rect_color=(128, 128, 128),
                    text="Cancel",
                    text_color=(0, 0, 0),
                    font_size=20,
                ),
                lambda: self.change_state(MenuState),
            ),
        }
        self.new_game_input_box = pygame.Rect((100, 300), (500, 200))
        self.new_game_input_box.center = (
            self.screen_width // 2,
            self.screen_height // 2,
        )
        self.new_game_input = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=self.new_game_input_box, manager=self.manager
        )

    def draw(self):
        """Performs all draw related tasks related to the "New Game" Menu."""

        # Gets delta time
        dt = self.clock.tick(30) / 1000

        # Renders and blits text
        new_game_txt = utils.font(51).render(
            "Enter File name for new game:", True, (0, 0, 0)
        )
        new_game_txt_rect = new_game_txt.get_rect(center=(self.screen_width // 2, 40))
        self.screen.blit(new_game_txt, new_game_txt_rect)

        # Draws buttons
        for dict_key, button in self.buttons.items():
            button[0].draw()

        self.manager.update(dt)
        self.manager.draw_ui(self.screen)

        pygame.display.update()

    def handle_events(self, event):
        """Handles all events related to thte "New Game" Menu."""

        mousex, mousey = pygame.mouse.get_pos()

        # Add effects on text input from pygame_gui
        self.new_game_input.enable()
        self.new_game_input.focus()
        self.new_game_input.rebuild_from_changed_theme_data()
        self.new_game_input.process_event(event)

        # Handles logic for buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            for key, button in self.buttons.items():
                if button[0].get_rect().collidepoint((mousex, mousey)):
                    button[1]()

    def okay(self):
        """Handles logic for the MenuButtons."""
        input_text = self.new_game_input.get_text()
        if input_text != "":
            print(f"Ze text you typed is: {input_text}\nRedirecting to game screen...")
            self.change_state(PlayingGameState)
        else:
            print(
                "No Text Selected, to be implemented (Or use placeholder text)\nRedirecting to main menu..."
            )
            self.change_state(MenuState)


class PlayingGameState(BaseState):
    """IMPORTANT: This state actually allows you to play the game, controlling your player (a snake)"""

    def __init__(self, game_class):
        super().__init__(game_class)

        # Initializes buttons, like MenuState
        self.buttons = {
            "pause_button": (
                [
                    ImageButton(self.screen, "pause.png", (750, 0), resize_to=(50, 50)),
                    ImageButton(self.screen, "play.png", (750, 0), resize_to=(50, 50)),
                ],
                NotImplemented,
            )
        }

        # Initializes other important components.
        # NOTE: Some will be converted to lists, to obtain multiple entities of that
        self.pause_menu = PauseMenu(game_class)
        self.background = utils.load_image("bg.png").convert()
        self.player = Player()
        self.enemy = HomingBulletEnemy(self.player)
        self.shop = ShopEntity()

        # Currently, each tile is a 800x600 pixel image. May be changed to a square (possibly 25x25) soon
        self.map = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ]

        # Sets some commonly used gamewide data
        game_data.player = self.player
        game_data.player_list["main_player"] = self.player
        game_data.playing_substate = self
        game_data.current_substate = self

    def draw(self):
        """Performs all draw related tasks related to the Main Game."""

        # If the current state is the playing state
        if game_data.current_substate.__class__ == self.__class__:
            self.draw_map()
            self.enemy.draw()
            self.shop.draw()
        else:
            # Otherwise, draw the substate with its .draw method
            game_data.current_substate.draw()

        # Draws the buttons
        for button in self.buttons.values():
            if self.pause_menu.draw_pause:
                button[0][1].draw()
            else:
                button[0][0].draw()

        # Draws player and potentially pause menu
        game_data.player.draw()
        self.pause_menu.draw()

    def draw_map(self):
        """Extra function, used to draw the map, based off of self.map."""
        self.screen.fill((135, 206, 235))
        for i, row in enumerate(self.map):
            for j, column in enumerate(row):
                if column == 1:
                    self.screen.blit(
                        self.background,
                        (
                            i * 800 - game_data.camera_offset[0],
                            j * 600 - game_data.camera_offset[1],
                        ),
                    )

    def handle_events(self, event):
        """Handles all events related to thte Main Game."""

        # Handles mouse presses and pause button presses
        mousex, mousey = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_name, button in self.buttons.items():
                if self.pause_menu.draw_pause:
                    if button[0][1].get_rect().collidepoint((mousex, mousey)):
                        self.pause_menu.toggle_menu()
                else:
                    if button[0][0].get_rect().collidepoint((mousex, mousey)):
                        self.pause_menu.toggle_menu()

        # Handles pause menu related events
        self.pause_menu.handle_events(event)

        # If game's not paused, and current state is the playing state
        # Handle the shop and enemy's events
        if (
            not self.pause_menu.draw_pause
            and game_data.current_substate.__class__ == self.__class__
        ):
            self.enemy.handle_events(event)
            self.shop.handle_events(event)
        # If the current state's not the playing state,
        # Handle the substate's events with its .handle_events() method
        elif game_data.current_substate.__class__ != self.__class__:
            game_data.current_substate.handle_events(event)

        game_data.player.handle_events(event)

    def constant_run(self):
        """Handles all things that will be run ONCE per frame in the Main Game."""
        if not self.pause_menu.draw_pause:
            game_data.player.constant_run()
            self.enemy.constant_run()
            self.shop.constant_run()


class PauseMenu(BaseState):
    def __init__(
        self,
        game_class,
        screen=common.SCREEN,
    ):
        super().__init__(game_class)

        self.screen = screen
        self.draw_pause = False

        self.screen_surf = pygame.Surface(  # lgtm [py/call/wrong-arguments]
            self.screen.get_size()
        )
        self.buttons = {
            "resume_button": (
                MenuButton(
                    self.screen,
                    (300, 200, 200, 100),
                    (128, 128, 128),
                    "Resume",
                    (0, 0, 0),
                    40,
                ),
                lambda: self.toggle_menu(),
            ),
            "quit_button": (
                MenuButton(
                    self.screen,
                    (300, 400, 200, 100),
                    (128, 128, 128),
                    "Quit Game",
                    (0, 0, 0),
                    40,
                ),
                lambda: self.change_state(MenuState),
            ),
        }
        self.alpha = 1
        self.max_alpha = 180

    def draw(self):
        if self.draw_pause:
            if self.alpha < self.max_alpha:
                self.fade(self.alpha)
            pause_txt = utils.font(60).render("Paused", True, (0, 0, 0))
            self.screen.blit(pause_txt, (300, 100))
            self.screen.blit(self.screen_surf, (0, 0))

            for button in self.buttons.values():
                button[0].draw()

    def fade(self, alpha):
        self.screen_surf.set_alpha(alpha)
        self.alpha += 40

    def handle_events(self, event):
        if self.draw_pause:
            mousex, mousey = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons.values():
                    if button[0].get_rect().collidepoint((mousex, mousey)):
                        button[1]()

    def toggle_menu(self):
        self.draw_pause = not self.draw_pause
        self.alpha = 0

    def change_state(self, other_state):
        self.game_class.state = other_state(self.game_class)
