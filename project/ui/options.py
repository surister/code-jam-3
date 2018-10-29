from pathlib import PurePath

import pygame as pg
from pygame.image import load

from project.constants import FPS, PATH_BUTTONS, PATH_CURSORS, PATH_IMAGES


class Options:

    def __init__(self, screen: pg.Surface):

        self.screen = screen
        self.background = load(str(PurePath(PATH_IMAGES).joinpath("background3.png")))
        self.sound = None

        self.back_btn = load(str(PurePath(PATH_BUTTONS).joinpath("back.png")))
        self.back_btn_rect = pg.Rect(20, 20, self.back_btn.get_width(), self.back_btn.get_height())
        self.back_btn_hover = False
        self.x = self.y = 0

        self.shift = 40
        self.cursor = load(str(PurePath(PATH_CURSORS).joinpath("cur.png"))).convert_alpha()
        self.cursor2 = load(str(PurePath(PATH_CURSORS).joinpath("hov.png"))).convert_alpha()

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

            pg.display.update()
        return running

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self._draw_back_button()

        if self.back_btn_hover:
            self.screen.blit(self.cursor2, (self.x, self.y))
        else:
            self.screen.blit(self.cursor, (self.x, self.y))

    def _draw_back_button(self)->None:
        self.back_btn_rect.left = 20
        self.back_btn_hover = self._hovered(self.x, self.y, self.back_btn_rect)

        if self.back_btn_hover:
            self.back_btn_rect.left = self.shift
        else:
            self.back_btn_rect.left = 20
        self.screen.blit(self.back_btn, self.back_btn_rect)

    def _hovered(self, x: int, y: int, button: pg.Rect)-> bool:
        return button.collidepoint(x, y)
