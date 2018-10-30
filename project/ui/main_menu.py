from pathlib import PurePath
from webbrowser import open

import pygame as pg
from pygame.image import load

from project.constants import BACKGROUND, BACKGROUND_3, BUTTONSHEET, CURSOR, CURSOR_HOVER, GIT_LAB_LINK, HEIGHT,\
    HOVER_SOUND, LOGO, PATH_BACKGROUNDS, PATH_BUTTONS, PATH_CURSORS, PATH_IMAGES, WIDTH
from project.ui.sheet import Sheet
from project.ui.volume import get_volume


class Home:

    def __init__(self, screen, paused: bool = False):

        self.screen = screen
        self.paused = paused
        # SCREEN: 1280x720px = WxH
        # devided by 5 parts horizontally - W/5 = 256px (slice)
        # devided by 8 parts vertically - H/8 = 90px (segment)

        self.slice = WIDTH // 5     # 256px
        self.segment = HEIGHT // 8  # 90px
        self.air = self.space = 10    # px
        self.shift = 20               # px

        self.sheet = Sheet(str(PurePath(PATH_BUTTONS).joinpath(BUTTONSHEET)))
        if self.paused:
            self.background = load(str(PurePath(PATH_BACKGROUNDS).joinpath(BACKGROUND_3))).convert_alpha()
        else:
            self.background = load(str(PurePath(PATH_BACKGROUNDS).joinpath(BACKGROUND))).convert_alpha()

        self.buttons_hover_states = {"play": False, "options": False, "about": False, "exit": False, "gitlab": False}
        self.buttons_sprites = {
            "play": self.sheet.get_image(0, 0, 384, 70, True),
            "options": self.sheet.get_image(0, 70, 320, 70, True),
            "about": self.sheet.get_image(0, 140, 320, 70, True),
            "exit": self.sheet.get_image(0, 210, 320, 70, True),
            "gitlab": self.sheet.get_image(320, 70, 100, 100, True),
            "gitlab_h": self.sheet.get_image(320, 170, 100, 100, True)}

        # LOGO: 768x360px
        # horizontal - logo takes 3 parts out of 5 - W/5 * 3 = 768px
        # vertical - logo takes half of H - H/2 = 360px
        self.logo_rect = pg.Rect(self.slice, 0, self.slice * 3, HEIGHT / 2)
        self.logo_image = load(str(PurePath(PATH_IMAGES).joinpath(LOGO))).convert_alpha()

        # PLAY BUTTON (larger) 384x70px
        # horizontal - one part and half of 5 = W/5 * 1.5 = 384px
        # vertical - 7 parts of 9 (of the segment) = S/9 * 7 = 70px
        # (10px for the air on top and the bottom)
        self.play_button_rect = \
            pg.Rect(self.space, self.segment * 4 + self.air, self.slice * 1.5, self.segment - (self.air * 2))

        # other buttons 320*70px
        # horizontal - one part and quarter of 5 = W/5 * 1.25 = 320px
        # vertical - 7 parts of 9 (of the segment) = S/9 * 7 = 70px
        # (10px for the air on top and the bottom)
        self.other_button_rect = \
            pg.Rect(self.space, self.segment * 5, self.slice * 1.25, self.segment - (self.air * 2))

        self.gitlab_button_rect = pg.Rect(WIDTH - 100 - 20, HEIGHT - 100 - 20, 200, 200)
        self.buttons_dict = {"options": 5, "about": 6, "exit": 7}

        self.sound = HOVER_SOUND
        self.sound.set_volume(get_volume())

        self.cursor = load(str(PurePath(PATH_CURSORS).joinpath(CURSOR))).convert_alpha()
        self.cursor2 = load(str(PurePath(PATH_CURSORS).joinpath(CURSOR_HOVER))).convert_alpha()
        self.once = True

    def draw(self)-> None:
        x, y = pg.mouse.get_pos()

        self._draw_background()

        self._draw_play_button(x, y)
        self._draw_gitlab_button(x, y)
        self._draw_other_buttons(x, y)

        self._play_sound()
        self._draw_cursor(x, y)

        pg.display.update()

    def _draw_background(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.logo_image, self.logo_rect)

    def _draw_cursor(self, x, y):
        if any(self.buttons_hover_states.values()):
            self.screen.blit(self.cursor2, (x, y))
        else:
            self.screen.blit(self.cursor, (x, y))

    def _draw_other_buttons(self, x, y):
        for key in self.buttons_dict.keys():
            self._draw_other_button(x, y, key)

    def _draw_play_button(self, x: int, y: int)-> None:
        self.play_button_rect.top = self.segment * 4
        self.play_button_rect.left = self.space
        hovered = self._hovered(x, y, self.play_button_rect)

        if hovered:
            self.buttons_hover_states["play"] = True
            self.play_button_rect.left = self.shift
            self.screen.blit(self.buttons_sprites["play"], self.play_button_rect)
        else:
            self.buttons_hover_states["play"] = False
            self.play_button_rect.left = self.space
            self.screen.blit(self.buttons_sprites["play"], self.play_button_rect)

    def _draw_other_button(self, x: int, y: int, button: str)-> None:
        self.other_button_rect.top = self.segment * self.buttons_dict[button]
        hovered = self._hovered(x, y, self.other_button_rect)

        if hovered:
            self.buttons_hover_states[button] = True
            self.other_button_rect.left = self.shift
            self.screen.blit(self.buttons_sprites[button], self.other_button_rect)
        else:
            self.buttons_hover_states[button] = False
            self.other_button_rect.left = self.space
            self.screen.blit(self.buttons_sprites[button], self.other_button_rect)

    def _draw_gitlab_button(self, x: int, y: int)-> None:
        hovered = self._hovered(x, y, self.gitlab_button_rect)

        if hovered:
            self.buttons_hover_states["gitlab"] = True
            self.screen.blit(self.buttons_sprites["gitlab_h"], self.gitlab_button_rect)
        else:
            self.buttons_hover_states["gitlab"] = False
            self.screen.blit(self.buttons_sprites["gitlab"], self.gitlab_button_rect)

    def _play_sound(self)-> None:
        if not any(self.buttons_hover_states.values()):
            self.once = True
        elif self.once:
            self.sound.play()
            self.once = False

    def update_volume(self)->None:
        self.sound.set_volume(get_volume())

    @staticmethod
    def _hovered(x: int, y: int, button: object)-> bool:
        return button.collidepoint(x, y)

    @staticmethod
    def open_gitlab()-> None:
        open(GIT_LAB_LINK)
