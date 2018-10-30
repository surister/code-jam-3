import json
import os
from pathlib import PurePath

import pygame as pg

from project.constants import HEIGHT, PATH_IMAGES, PATH_PROJECT, PATH_VOICES, WIDTH
from project.ui.sheet import Sheet
from project.ui.volume import get_volume


def json_load():
    with open(str(PurePath(PATH_PROJECT).joinpath("data.json"))) as f:
        DATA = json.load(f)
    return DATA


class Intro:

    def __init__(self, screen: pg.Surface):

        pg.mixer.init()
        self.screen = screen
        self.playing = True

        self.slides_sheet = Sheet(str(PurePath(PATH_IMAGES).joinpath("slidesheet.png")))
        self.slides = [self.slides_sheet.get_image(0, HEIGHT * i, WIDTH, HEIGHT) for i in range(0, 3)]

        self.voice_clips = [pg.mixer.Sound(str(PurePath(PATH_VOICES).joinpath(i)))
                            for i in os.listdir(str(PurePath(PATH_VOICES)))]

        volume = get_volume()
        self.voice_clips[0].set_volume(volume)
        self.voice_clips[1].set_volume(volume)
        self.voice_clips[2].set_volume(volume)

        self.durations = [i.get_length() for i in self.voice_clips]
        self.durations[0] += 1.5

        self.start_time = pg.time.get_ticks()
        self.index = 0
        self.once = True

    def play(self):

        current_time = (pg.time.get_ticks() - self.start_time) / 1000

        if current_time > self.durations[self.index]:
            self.index += 1
            self.start_time = pg.time.get_ticks()
            self.once = True

        if self.index == 3:
            self.playing = False
            self._played()
            return

        if self.once:
            self.voice_clips[self.index].play()
            self.once = False

        self.screen.blit(self.slides[self.index], (0, 0))
        pg.display.flip()

    def _played(self):
        import json

        file = str(PurePath(PATH_PROJECT).joinpath("data.json"))

        with open(file, "r") as f:
            data = json.load(f)
            data["intro_played"] = True

        with open(file, "w") as f:
            json.dump(data, f)
