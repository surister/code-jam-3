from pathlib import PurePath

import pygame as pg
from pygame.math import Vector2 as Vec

from project.constants import Color, HEALTHBAR, PATH_IMAGES


class StaticHealthbar(pg.sprite.Sprite):

    def __init__(self, game, owner, x: int, y: int, width=None):
        super().__init__()
        self.game = game
        self.owner = owner
        self.screen = self.game.screen
        self.add(self.game.all_sprites)
        self.game.nonsprite.add(self)
        self.x = x
        self.y = y
        self.width = width

        self.image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(HEALTHBAR))).convert_alpha()
        self.image = pg.transform.scale(self.image, (250, 100))
        self.image.set_colorkey(Color.black)
        self.rect = self.image.get_rect()
        self.rect.center = Vec(200, 40)

    def draw(self) -> None:

        self.hp = self.owner.health
        self.sp = self.owner.shield

        hp_color = Color.pure_green
        sp_color = Color.pure_blue
        if self.hp <= 0:
            self.hp = 0

        if self.hp < 40:
            hp_color = Color.red
        pg.draw.rect(self.screen, hp_color, [100, 20, self.hp*1.75, 30])

        if self.sp is not None:
            pg.draw.rect(self.screen, sp_color, [70, 80, self.sp*2, 20])


class MovableHealtbar(pg.sprite.Sprite):

    def __init__(self, game, owner, x: int, y: int):
        super().__init__()
        self.game = game
        self.add(self.game.all_sprites)
        self.owner = owner
        self.screen = self.game.screen
        self.image = pg.Surface((100, 20))

        self.rect = self.image.get_rect()

        self.pos = Vec(x, y)

    def update(self):
        if self.owner.health != 20:
            self.image = pg.Surface((self.owner.health*2, 10))
            self.image.fill(Color.red)
            self.pos.x = self.owner.pos.x + 30
            self.pos.y = self.owner.pos.y + 30
            self.rect.midbottom = self.pos

            self.game.screen.blit(self.image, self.rect)
