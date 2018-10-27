from pathlib import PurePath

import pygame as pg

from project.constants import Color, MINE_IMAGE_NAME, PATH_IMAGES
from project.sprites.combat import Combat


class Mine(Combat, pg.sprite.Sprite):
    """ Mines slowly move to the asteroid, exploding on impact of asteroid or player. """

    def __init__(
        self,
        game: 'Game',
        vel: int,
        pos: int,
        points: int=150
    ):
        Combat.__init__(self, 30, points=points)
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.vel = vel
        self.pos = pos

        self.image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(MINE_IMAGE_NAME)))
        self.rect = self.image.get_rect()

        self.add(self.game.all_sprites, self.game.enemy_sprites)

        self.image.set_colorkey(Color.black)
        # self.healthbar = MovableHealtbar(self.game, self, self.pos.x, self.pos.y)

    def update(self):
        """ Move left untill off screen """
        self.pos.x = self.pos.x - self.vel.x
        if self.pos.x < 0:
            self.kill()
        self.rect.midbottom = self.pos

        # self.healthbar = Healthbar(game=self.game, owner=self, x=self.pos.x - 500, y=self.pos.y)

        super().update()
