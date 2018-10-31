from pathlib import PurePath

import pygame as pg

from project.constants import Color, PATH_FONTS


class ScoreDisplay:

    def __init__(self, game, x: int, y: int, font: str, font_size: int):
        self.game = game
        self.screen = self.game.screen
        self.game.nonsprite.add(self)

        self.x = x
        self.y = y

        self.font = pg.font.Font(str(PurePath(PATH_FONTS).joinpath(font)), font_size)

    def draw(self)->None:
        if self.game.score >= 1000000:
            score_text = '9999999'
        else:
            score_text = str(self.game.score).zfill(7)
        text = self.font.render(score_text, True, Color.white)
        self.screen.blit(text, (self.x, self.y))
