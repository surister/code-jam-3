import json
from pathlib import PurePath

import pygame as pg
from pygame.image import load

from project.constants import BACKGROUND_3, BACK_BUTTON, CURSOR, CURSOR_HOVER, FPS, HOVER_SOUND, PATH_BACKGROUNDS,\
    PATH_BUTTONS, PATH_CURSORS, PATH_PROJECT, SWITCH, VOLUME, VOLUME_NO
from project.ui.volume import get_volume


class Options:
    """
    Represents the options page.

    The about page contains buttons for controling the volume and the playing of the intro.
    """

    def __init__(self, screen: pg.Surface):
        """
        Constructor for the options page.
        """
        self.screen = screen
        self.background = load(str(PurePath(PATH_BACKGROUNDS).joinpath(BACKGROUND_3)))
        self.sound = None

        self.back_btn = load(str(PurePath(PATH_BUTTONS).joinpath(BACK_BUTTON)))
        self.back_btn_rect = pg.Rect(20, 20, self.back_btn.get_width(), self.back_btn.get_height())
        self.back_btn_hover = False

        self.x = self.y = 0
        self.mouseclick = False

        self.shift = 40
        self.cursor = load(str(PurePath(PATH_CURSORS).joinpath(CURSOR))).convert_alpha()
        self.cursor2 = load(str(PurePath(PATH_CURSORS).joinpath(CURSOR_HOVER))).convert_alpha()

        self.volume = load(str(PurePath(PATH_BUTTONS).joinpath(VOLUME))).convert_alpha()
        self.novolume = load(str(PurePath(PATH_BUTTONS).joinpath(VOLUME_NO))).convert_alpha()

        self.switch = load(str(PurePath(PATH_BUTTONS).joinpath(SWITCH))).convert_alpha()
        self.switch_rect = pg.Rect(self._volume_to_pixels(), 150, self.switch.get_width(), self.switch.get_height())
        self.clicked_switch = False

        self.intro_played = self._intro_state()
        self.intro_button_on = load(str(PurePath(PATH_BUTTONS).joinpath("on_btn.png"))).convert_alpha()
        self.intro_button_off = load(str(PurePath(PATH_BUTTONS).joinpath("off_btn.png"))).convert_alpha()
        self.intro_hovered = False

        self.on = load(str(PurePath(PATH_BUTTONS).joinpath("on.png"))).convert_alpha()
        self.off = load(str(PurePath(PATH_BUTTONS).joinpath("off.png"))).convert_alpha()
        self.intro_img = load(str(PurePath(PATH_BUTTONS).joinpath("intro.png"))).convert_alpha()

        self.on = pg.transform.scale(self.on, (100, 50))
        self.off = pg.transform.scale(self.off, (100, 50))

        self.sound = HOVER_SOUND
        self.sound.set_volume(get_volume())

        self.once = True
        self.mute = None

    def handle_input(self)->None:
        """
        Handling the events.
        Clicking on a button/quiting the game.
        """
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
                if event.type == pg.MOUSEBUTTONUP and self.intro_hovered:
                    self.intro_played = not self.intro_played
            self._pixels_to_volume()
            self._save_intro_state()
            pg.display.update()
        return running

    def draw(self):
        """
        Unifying drawing method - draws every element of the options page.
        """
        self._draw_background()

        self._draw_back_button()
        self._draw_volume()
        self._draw_switch()
        self._draw_intro()

        self._play_sound()
        self._draw_cursor()

    def _draw_background(self):
        """
        Bliting the background image and the on the screen.
        """
        self.screen.blit(self.background, (0, 0))

    def _draw_cursor(self):
        """
        Bliting the cursor on the screen.
        Classical cursor and finger cursor (if any hoverable element is hovered).
        """
        if self.back_btn_hover or self.clicked_switch or self.intro_hovered:
            self.screen.blit(self.cursor2, (self.x, self.y))
        else:
            self.screen.blit(self.cursor, (self.x, self.y))

    def _draw_volume(self)->None:
        """
        Bliting the volume bar on the screen.
        """
        if 120 < self.switch_rect.left < 133:
            self.screen.blit(self.novolume, (20, 140))
            self.mute = True
        else:
            self.screen.blit(self.volume, (20, 140))
            self.mute = False

    def _draw_intro(self)->None:
        """
        Bliting the intro labels on the screen. (INRO, ON, OFF).
        """
        self.intro_hovered = self._hovered(self.x, self.y, pg.Rect(920, 150, 200, 100))

        if self.intro_played:
            self.screen.blit(self.intro_button_on, (920, 150))
        else:
            self.screen.blit(self.intro_button_off, (920, 150))

        self.screen.blit(self.intro_img, (875, 50))
        self.screen.blit(self.off, (810, 170))
        self.screen.blit(self.on, (1120, 170))

    def _intro_state(self)->True:
        """
        Extracting the intro state (on or off) from the data.json file.
        """
        with open(str(PurePath(PATH_PROJECT).joinpath("data.json"))) as f:
            data = json.load(f)
            played = data["intro_played"]
        return played

    def _save_intro_state(self)->None:
        """
        Saving the intro state (on or off) to the data.json file.
        """
        with open(str(PurePath(PATH_PROJECT).joinpath("data.json"))) as f:
            data = json.load(f)

        with open(str(PurePath(PATH_PROJECT).joinpath("data.json")), "w") as f:
            data["intro_played"] = self.intro_played
            json.dump(data, f)

    def _draw_switch(self)->None:
        """
        Bliting the volume switching button on the screen.
        Ensuring that is in the borders of the volume bar.
        """
        if self._hovered(self.x, self.y, self.switch_rect) and self.mouseclick:
            self.clicked_switch = True

        if self.mouseclick and self.clicked_switch:
            if 122 < self.x < 695:
                self.switch_rect.left = self.x
        else:
            self.clicked_switch = False

        self.screen.blit(self.switch, self.switch_rect)

    def _draw_back_button(self)->None:
        """
        Bliting the back button on the screen.
        Shifting to the right if it is hovered.
        """
        self.back_btn_rect.left = 20
        self.back_btn_hover = self._hovered(self.x, self.y, self.back_btn_rect)

        if self.back_btn_hover:
            self.back_btn_rect.left = self.shift
        else:
            self.back_btn_rect.left = 20
        self.screen.blit(self.back_btn, self.back_btn_rect)

    def _volume_to_pixels(self)->int:
        """
        Converting the volume value from the data.json file to pixels for the volume bar.
        """
        with open(str(PurePath(PATH_PROJECT).joinpath("data.json"))) as f:
            data = json.load(f)
        return 122 + int(data["volume"] * 5.7)

    def _pixels_to_volume(self)->None:
        """
        Converting the pixels for volume and saving it to the data.json file.
        """
        with open(str(PurePath(PATH_PROJECT).joinpath("data.json"))) as f:
            data = json.load(f)

        with open(str(PurePath(PATH_PROJECT).joinpath("data.json")), "w") as f:
            data["volume"] = (self.switch_rect.left - 122) // 5.7
            data["mute"] = self.mute
            json.dump(data, f)

    def _play_sound(self)->None:
        """
        Playing the sound if any hoverable element is hovered.
        Ensuring the current volume coresponds to the value in the data.json file.
        """
        self.sound.set_volume(get_volume())

        if not self.back_btn_hover:
            self.once = True
        elif self.once:
            self.sound.play()
            self.once = False

    def _hovered(self, x: int, y: int, button: pg.Rect)-> bool:
        """
        Wraper for collidepoint (checks if point is in pygame.Rect object).
        """
        return button.collidepoint(x, y)
