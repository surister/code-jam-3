import math
from collections import deque
from pathlib import PurePath
from typing import Union

import pygame as pg

from project.constants import Color, PATH_IMAGES, PROJECTILE_IMAGE_NAME
from project.sprites.combat import Combat
from project.sprites.sprite_internals import Physics

FIGHTER_PROJECTILE_IMAGE = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(PROJECTILE_IMAGE_NAME)))


class Fighter(Combat, Physics, pg.sprite.Sprite):
    """ Fighters circle around the player and rapidly shoot weak projectiles at him """
    def __init__(
        self,
        game,
        radius: int,
        friction: Union[int, float],
        vel: pg.Vector2,
        pos: pg.Vector2,
        points: int=50,
        image: pg.Surface= None
    ):
        Combat.__init__(self, 15, points=points)
        Physics.__init__(self, friction)
        # pg.sprite.Sprite.__init__(self)
        self.radius = radius
        self.pos = pos
        self.vel = vel
        self.acc = pg.Vector2(0, 0)
        self.game = game

        self.add(self.game.all_sprites)
        self.add(self.game.enemy_sprites)

        if image is None:
            self.image = pg.Surface((40, 40))
            self.image.fill(Color.light_green)
        else:
            self.image = image
        self.rect = self.image.get_rect()

        self.image.set_colorkey(Color.red)

        self.projectiles = deque()
        self.projectile_image = FIGHTER_PROJECTILE_IMAGE
        self.evil = True

    def update(self):
        player_pos = self.game.devchar.pos

        angle = math.atan2(player_pos.x - self.pos.x, self.pos.y - player_pos.y)
        if angle < 0:
            angle += math.tau

        self.acc.x = self.acc.y = 0
        self.acc.y -= math.cos(angle/math.tau*360)
        self.acc.x += math.sin(angle/math.tau*360)

        self._shot(-1)
        super().update()
