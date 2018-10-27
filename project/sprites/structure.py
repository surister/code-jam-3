import math
from collections import deque

import pygame as pg

from project.constants import Color
from project.sprites.combat import Combat
from project.ui.character_interface import MovableHealtbar


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
        self.type = 0

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
        self.evil = True
        self.healthbar = MovableHealtbar(self.game, self, self.pos.x, self.pos.y)

    def update(self) -> None:
        """ Move left untill destination passed if not already there, otherwise shoot at the player """
        if not self.arrived:
            self.pos.x = self.pos.x - self.vel.x

            if self.pos.x < self.destination:
                self.arrived = True
        else:
            angle = math.atan2(self.pos.y - self.game.devchar.pos.y, -(self.pos.x - self.game.devchar.pos.x))
            self._shot(angle, self.rect.midleft)

        self.rect.midbottom = self.pos
        super().update()
