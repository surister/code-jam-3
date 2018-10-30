import webbrowser as wb
from pathlib import PurePath

import pygame as pg
from pygame.image import load

from project.constants import BACKGROUND_2, BACK_BUTTON, CURSOR, CURSOR_HOVER, FPS, HOVER_SOUND, LABEL,\
    MISTY_HATS_LOGO, MISTY_HATS_LOGO_HOVER, MISTY_LINK, PATH_BACKGROUNDS, PATH_BUTTONS, PATH_CURSORS, PATH_IMAGES, PYTHON_DISCORD_LINK,\
    PYTHON_LOGO, PYTHON_LOGO_HOVER
from project.ui.volume import get_volume

# IF YOU ARE A MUGGLE DON'T LOOK AT THE CODE BECAUSE THERE ARE A LOT OF MAGIC NUMBERS


class About:

    def __init__(self, screen: pg.Surface):

        self.screen = screen
        self.background = load(str(PurePath(PATH_BACKGROUNDS).joinpath(BACKGROUND_2)))
        self.sound = None

        self.back_btn = load(str(PurePath(PATH_BUTTONS).joinpath(BACK_BUTTON)))
        self.back_btn_rect = pg.Rect(20, 20, self.back_btn.get_width(), self.back_btn.get_height())
        self.back_btn_hover = False
        self.x = self.y = 0

        self.shift = 40
        self.cursor = load(str(PurePath(PATH_CURSORS).joinpath(CURSOR))).convert_alpha()
        self.cursor2 = load(str(PurePath(PATH_CURSORS).joinpath(CURSOR_HOVER))).convert_alpha()

        self.label = load(str(PurePath(PATH_IMAGES).joinpath(LABEL))).convert_alpha()

        self.python_logo = load(str(PurePath(PATH_IMAGES).joinpath(PYTHON_LOGO))).convert_alpha()
        self.python_logo_hover = load(str(PurePath(PATH_IMAGES).joinpath(PYTHON_LOGO_HOVER))).convert_alpha()
        self.python_logo_hovered = False

        self.misty_logo = load(str(PurePath(PATH_IMAGES).joinpath(MISTY_HATS_LOGO))).convert_alpha()
        self.misty_logo_hover = load(str(PurePath(PATH_IMAGES).joinpath(MISTY_HATS_LOGO_HOVER))).convert_alpha()
        self.misty_logo_hovered = False

        self.sound = HOVER_SOUND
        self.sound.set_volume(get_volume())

    def handle_input(self)->None:

        clock = pg.time.Clock()
        waiting = True
        running = True

        while waiting:
            clock.tick(FPS/2)
            self.draw()
            self.x, self.y = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = running = False
                if event.type == pg.MOUSEBUTTONUP and self.back_btn_hover:
                    waiting = False
                if event.type == pg.MOUSEBUTTONUP and self.python_logo_hovered:
                    wb.open(PYTHON_DISCORD_LINK)
                if event.type == pg.MOUSEBUTTONUP and self.misty_logo_hovered:
                    wb.open(MISTY_LINK)
            pg.display.update()
        return running

    def draw(self):
        self._draw_background()

        self._draw_python_logo()
        self._draw_misty_logo()
        self._draw_back_button()

        self._play_sound()
        self._draw_cursor()

    def _draw_cursor(self):
        if any((self.back_btn_hover, self.python_logo_hovered, self.misty_logo_hovered)):
            self.screen.blit(self.cursor2, (self.x, self.y))
        else:
            self.screen.blit(self.cursor, (self.x, self.y))

    def _draw_background(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.label, (0, 0))

    def _draw_back_button(self)->None:
        self.back_btn_rect.left = 20
        self.back_btn_hover = self._hovered(self.x, self.y, self.back_btn_rect)

        if self.back_btn_hover:
            self.back_btn_rect.left = self.shift
        else:
            self.back_btn_rect.left = 20
        self.screen.blit(self.back_btn, self.back_btn_rect)

    def _draw_python_logo(self)->None:
        if self._hovered(self.x, self.y, pg.Rect(940, 600, 940 + 318, 600 + 111)):
            self.python_logo_hovered = True
            self.screen.blit(self.python_logo_hover, (940, 600))
        else:
            self.python_logo_hovered = False
            self.screen.blit(self.python_logo, (940, 600))

    def _draw_misty_logo(self)->None:
        if self._hovered(self.x, self.y, pg.Rect(40, 200, 120, 120)):
            self.misty_logo_hovered = True
            self.screen.blit(self.misty_logo_hover, (40, 200))
        else:
            self.misty_logo_hovered = False
            self.screen.blit(self.misty_logo, (40, 200))

    def _play_sound(self)->None:

        if not any([self.back_btn_hover, self.misty_logo_hovered, self.python_logo_hovered]):
            self.once = True
        elif self.once:
            self.sound.play()
            self.once = False

    def _hovered(self, x: int, y: int, button: pg.Rect)-> bool:
        return button.collidepoint(x, y)
