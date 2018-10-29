import pygame as pg

from project.constants import Color


class ScoreDisplay:

    def __init__(self, game: 'Game', x: int, y: int, font: str, font_size: str):
        self.game = game
        self.screen = self.game.screen
        self.game.nonsprite.add(self)

        self.x = x
        self.y = y

        self.font = pg.font.SysFont(font, font_size)

    def draw(self)->None:

        text = self.font.render(str(self.game.score).zfill(7), True, Color.white)
        self.screen.blit(text, (self.x, self.y))