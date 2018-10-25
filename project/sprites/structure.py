from collections import deque
from pathlib import PurePath

import pygame as pg

from project.constants import Color, PATH_IMAGES, PROJECTILE_IMAGE_NAME
from project.sprites.combat import Combat

STRUCTURE_PROJECTILE_IMAGE = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(PROJECTILE_IMAGE_NAME)))


class Structure(Combat, pg.sprite.Sprite):
    """ Structures slow move from off screen to their fixed position and then start firing at the player. """

    def __init__(
        self,
        game,
        destination: int,
        vel,
        pos,
        points: int=200,
        image: pg.Surface= None
    ):
        Combat.__init__(self, 20, points=points)
        pg.sprite.Sprite.__init__(self)
        self.destination = destination
        self.arrived = False
        self.game = game
        self.vel = vel
        self.pos = pos

        if image is None:
            self.image = pg.Surface((80, 80))
            self.image.fill(Color.red)
        else:
            self.image = image

        self.rect = self.image.get_rect()

        self.add(self.game.all_sprites)
        self.add(self.game.enemy_sprites)

        self.image.set_colorkey(Color.black)
        self.projectiles = deque()
        self.projectile_image = STRUCTURE_PROJECTILE_IMAGE
        self.evil = True

    def update(self):
        """ Move left untill destination passed if not already there, otherwise shoot at the player """
        if not self.arrived:
            self.pos.x = self.pos.x - self.vel.x

            if self.pos.x < self.destination:
                self.arrived = True
        else:
            # Fires straight to the left
            self._shot(-1)

        self.rect.midbottom = self.pos
        super().update()
