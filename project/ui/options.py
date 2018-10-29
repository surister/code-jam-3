import json
from pathlib import PurePath

import pygame as pg
from pygame.image import load

from project.constants import FPS, PATH_BUTTONS, PATH_CURSORS, PATH_GUI, PATH_IMAGES, PATH_PROJECT


class Options:

    def __init__(self, screen: pg.Surface):

        self.screen = screen
        self.background = load(str(PurePath(PATH_IMAGES).joinpath("background3.png")))
        self.sound = None

        self.back_btn = load(str(PurePath(PATH_BUTTONS).joinpath("back.png")))
        self.back_btn_rect = pg.Rect(20, 20, self.back_btn.get_width(), self.back_btn.get_height())
        self.back_btn_hover = False

        self.x = self.y = 0
        self.mouseclick = False

        self.shift = 40
        self.cursor = load(str(PurePath(PATH_CURSORS).joinpath("cur.png"))).convert_alpha()
        self.cursor2 = load(str(PurePath(PATH_CURSORS).joinpath("hov.png"))).convert_alpha()

        self.volume = load(str(PurePath(PATH_GUI).joinpath("volume.png"))).convert_alpha()
        self.novolume = load(str(PurePath(PATH_GUI).joinpath("novolume.png"))).convert_alpha()

        self.switch = load(str(PurePath(PATH_GUI).joinpath("switch.png"))).convert_alpha()
        self.switch_rect = pg.Rect(self._volume_to_pixels(), 150, self.switch.get_width(), self.switch.get_height())
        self.clicked_switch = False

        self.mute = None

    def handle_input(self)->None:

        clock = pg.time.Clock()
        waiting = True
        running = True

        while waiting:
            clock.tick(FPS/2)
            self.draw()
            self.x, self.y = pg.mouse.get_pos()

            for event in pg.event.get():
                self.mouseclick = pg.mouse.get_pressed()[0]

                if event.type == pg.QUIT:
                    waiting = running = False
                if event.type == pg.MOUSEBUTTONUP and self.back_btn_hover:
                    waiting = False

            pg.display.update()
        self._pixels_to_volume()
        return running

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self._draw_back_button()
        self._draw_volume()
        self._draw_switch()

        if self.back_btn_hover or self.clicked_switch:
            self.screen.blit(self.cursor2, (self.x, self.y))
        else:
            self.screen.blit(self.cursor, (self.x, self.y))

    def _draw_volume(self)->None:

        if 120 < self.switch_rect.left < 133:
            self.screen.blit(self.novolume, (20, 140))
            self.mute = True
        else:
            self.screen.blit(self.volume, (20, 140))
            self.mute = False

    def _draw_switch(self)->None:

        if self._hovered(self.x, self.y, self.switch_rect) and self.mouseclick:
            self.clicked_switch = True

        if self.mouseclick and self.clicked_switch:
            if 122 < self.x < 695:
                self.switch_rect.left = self.x
        else:
            self.clicked_switch = False

        self.screen.blit(self.switch, self.switch_rect)

    def _draw_back_button(self)->None:
        self.back_btn_rect.left = 20
        self.back_btn_hover = self._hovered(self.x, self.y, self.back_btn_rect)

        if self.back_btn_hover:
            self.back_btn_rect.left = self.shift
        else:
            self.back_btn_rect.left = 20
        self.screen.blit(self.back_btn, self.back_btn_rect)

    def _volume_to_pixels(self)->int:
        with open(str(PurePath(PATH_PROJECT).joinpath("data.json"))) as f:
            data = json.load(f)
        return 122 + int(data["volume"] * 5.7)

    def _pixels_to_volume(self)->None:
        with open(str(PurePath(PATH_PROJECT).joinpath("data.json"))) as f:
            data = json.load(f)

        with open(str(PurePath(PATH_PROJECT).joinpath("data.json")), "w") as f:
            data["volume"] = (self.switch_rect.left - 122) // 5.7
            data["mute"] = self.mute
            json.dump(data, f)

    def _hovered(self, x: int, y: int, button: pg.Rect)-> bool:
        return button.collidepoint(x, y)
