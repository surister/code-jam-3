import math
from collections import deque
from pathlib import PurePath
from typing import Union

import pygame as pg

from project.constants import FIGHTER_IMAGE_NAME, PATH_IMAGES
from project.sprites.combat import Combat
from project.sprites.sprite_internals import Physics
from project.ui.character_interface import DynamicHealthbar


class Fighter(Combat, Physics, pg.sprite.Sprite):
    """ Fighters circle around the player and rapidly shoot weak projectiles at him """
    def __init__(
        self,
        game,
        radius: int,
        friction: Union[int, float],
        vel: pg.Vector2,
        pos: pg.Vector2,
        points: int=50
    ):
        Combat.__init__(self, 15, points=points)
        Physics.__init__(self, friction)
        # pg.sprite.Sprite.__init__(self)
        self.radius = radius
        self.pos = pos
        self.vel = vel
        self.acc = pg.Vector2(0, 0)
        self.game = game
        self.type = 2
        self.projectile_scale = 0.5
        self.add(self.game.all_sprites, self.game.enemy_sprites)

        self.image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(FIGHTER_IMAGE_NAME)))

        self.base_image = self.image

        self.rect = self.image.get_rect()

        # self.image.set_colorkey(Color.red)

        self.projectiles = deque()
        self.evil = True
        self.healthbar = DynamicHealthbar(self.game, self)

    def update(self):

        angle = math.atan2(self.pos.y - self.game.devchar.pos.y, -(self.pos.x - self.game.devchar.pos.x))
        # -90 extra becasue of how the image is aligned
        self.image = pg.transform.rotate(self.base_image, angle * 180 / math.pi + -90)

        # self.acc.x = self.acc.y = 0
        self.acc.y = -math.sin(angle)
        self.acc.x = math.cos(angle)
        self._shot(angle, self.rect.midleft)
        super().update()
