import pygame as pg

from project.constants import Color


class Timer:

    def __init__(self, game, time: int, x: int, y: int, font: str, font_size: int):
        self.game = game
        self.screen = self.game.screen
        self.game.nonsprite.add(self)

        self.x = x
        self.y = y

        self.font = pg.font.SysFont(font, font_size)
        self.time = time
        self.start = pg.time.get_ticks()
        self.completed = False

    def draw(self)->None:
        if not self.completed:
            self.current = (pg.time.get_ticks() - self.start) // 1000
            if self.current <= self.time:
                self.text = self.font.render(self.min_sec(self.time - self.current), True, Color.white)

                self.screen.blit(self.text, (self.x, self.y))

    @staticmethod
    def min_sec(sec: int)->str:
        return f"{int((sec - sec % 60) / 60)}:{sec % 60:02}"
