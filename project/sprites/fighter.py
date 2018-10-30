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
    """
    Represents a fighters that circle around the player and rapidly shoot weak projectiles at him
    """

    def __init__(
        self,
        game,
        friction: Union[int, float],
        pos: pg.Vector2,
        points: int=50,
        health: int=15,
        attack: int=2
    ):
        Combat.__init__(self, health, points=points, attack=attack)
        Physics.__init__(self, friction)
        self.pos = pos
        self.acc = pg.Vector2(0, 0)
        self.vel = pg.Vector2(0, 0)
        self.game = game
        self.type = 2
        self.projectile_scale = 0.5
        self.add(self.game.all_sprites, self.game.enemy_sprites)

        self.image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(FIGHTER_IMAGE_NAME)))

        self.base_image = self.image

        self.rect = self.image.get_rect()

        self.projectiles = deque()
        self.evil = True
        self.healthbar = DynamicHealthbar(self.game, self)
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        """
        Overrides pg.sprite.Sprite update function and gets called in /game.py/Game class

        Turn towards the player and let the Physics do the rest
        """
        angle = math.atan2(self.pos.y - self.game.devchar.pos.y, - (self.pos.x - self.game.devchar.pos.x))
        # -90 extra because of how the image is aligned
        self.image = pg.transform.rotate(self.base_image, angle * 180 / math.pi + -90)

        self.acc.y = -math.sin(angle)
        self.acc.x = math.cos(angle)
        self._shot(angle, self.rect.midleft)
        super().update()
