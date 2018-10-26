import pygame as pg

from project.constants import Color


class Healthbar:

    def __init__(self, game, owner, screen, x: int, y: int, width=None):
        super().__init__()
        self.game = game
        self.owner = owner
        self.screen = screen

        self.x = x
        self.y = y
        self.game.nonsprite.add(self)

    def draw(self) -> None:

        self.hp = self.owner.health
        self.sp = self.owner.shield

        hp_color = Color.pure_green
        sp_color = Color.pure_blue
        if self.hp < 40:
            hp_color = Color.red
        pg.draw.rect(self.screen, hp_color, [self.x, self.y, self.hp*2, 20])

        if self.hp is not None:
            pg.draw.rect(self.screen, sp_color, [70, 80, self.sp*2, 20])


class MovableHealtbar(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
