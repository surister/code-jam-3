import math
from collections import deque
from pathlib import PurePath

import pygame as pg

from project.constants import Color, PATH_IMAGES, STRUCTURE_IMAGE_NAME
from project.sprites.combat import Combat
from project.ui.character_interface import DynamicHealthbar


class Structure(Combat, pg.sprite.Sprite):
    """ Structures slow move from off screen to their fixed position and then start firing at the player. """

    def __init__(
        self,
        game,
        destination: int,
        vel: pg.math.Vector2,
        pos: pg.math.Vector2,
        health: int=10,
        points: int=200
    ):
        Combat.__init__(self, health, points=points)
        pg.sprite.Sprite.__init__(self)
        self.destination = destination
        self.arrived = False
        self.game = game
        self.vel = vel
        self.pos = pos
        self.type = 2
        print(self.pos)
        self.image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(STRUCTURE_IMAGE_NAME)))
        self.rect = self.image.get_rect()

        self.add(self.game.all_sprites, self.game.enemy_sprites)

        self.image.set_colorkey(Color.black)
        self.projectiles = deque()
        self.evil = True
        self.healthbar = DynamicHealthbar(self.game, self)
        self.mask = pg.mask.from_surface(self.image)

        self.rect = self.image.get_rect(center=self.pos)

    def update(self) -> None:
        """ Move left untill destination passed if not already there, otherwise shoot at the player """
        if not self.arrived:
            self.pos.x = self.pos.x - self.vel.x

            if self.pos.x < self.destination:
                self.arrived = True
        else:
            angle = math.atan2(self.pos.y - self.game.devchar.pos.y, - (self.pos.x - self.game.devchar.pos.x))
            self._shot(angle, self.rect.midleft)

        self.rect.midbottom = self.pos
        super().update()
