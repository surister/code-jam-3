import pygame as pg

from project.constants import Color


class Healthbar:

    def __init__(self, game, owner, screen, hp, x, y):
        super().__init__()
        self.game = game
        self.owner = owner
        self.screen = screen
        self.hp = hp
        self.x = x
        self.y = y

    def draw(self, hp: int, sp: int = None) -> None:
        hp_color = Color.pure_green
        sp_color = Color.pure_blue
        if hp < 40:
            hp_color = Color.red
        pg.draw.rect(self.screen, hp_color, [70, 40, hp*2, 20])

        if sp is not None:
            pg.draw.rect(self.screen, sp_color, [70, 80, sp*2, 20])
