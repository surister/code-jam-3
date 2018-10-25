from collections import deque
from pathlib import PurePath
from typing import Union

import pygame as pg

from project.constants import Color, PATH_IMAGES, PROJECTILE_IMAGE_NAME, SHOOT_RATE, PLAYER_ACC
from project.sprites.game_elements import Projectile
from project.sprites.physics import Physics


class Character(Physics, pg.sprite.Sprite):
    """ Base class for Character, current implementation based on dev_character """

    def __init__(
        self,
        game,
        health_points: int,
        defense: int,
        pos: pg.Vector2 = None,
        acc: pg.Vector2 = None,
        vel: pg.Vector2 = None,
        weapons: list = None,
        friction: Union[int, float] = 1,
        image: pg.Surface = None
    ):

        super().__init__()
        self.game = game
        self.add(self.game.all_sprites)

        self.player_acc = PLAYER_ACC
        self.shoot_rate = SHOOT_RATE

        self.projectiles = deque()

        self.rapid_fire = True
        if self.rapid_fire:
            self.shoot_rate -= 20

        self.health_points = health_points
        self.defense = defense

        self.last_update = 0

        if image is None:
            self.image = pg.Surface((50, 50))
            self.image.fill(Color.white)
        else:
            self.image = image
        self.rect = self.image.get_rect()

        if weapons is None:
            self.weapons = []
        else:
            self.weapons = weapons

        if pos is None:
            self.pos = pg.Vector2(0, 0)
        else:
            self.pos = pos

        if acc is None:
            self.acc = pg.Vector2(0, 0)
        else:
            self.acc = acc

        if vel is None:
            self.vel = pg.Vector2(0, 0)
        else:
            self.vel = vel

        self.friction = friction

        self.image.set_colorkey(Color.green)
        self.pos = pg.Vector2(500, 500)

    def _shot(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.shoot_rate:
            self.last_update = now
            image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(PROJECTILE_IMAGE_NAME)))
            # TODO we load the image in every shot? hmhm that doesn't sound efficient
            self.projectiles.append(Projectile(self.game, self, image=image))

    def update(self) -> None:

        self.key = pg.key.get_pressed()

        self.acc.y = self.acc.x = 0
        if self.key[pg.K_UP] or self.key[pg.K_w]:
            self.acc.y = -self.player_acc
        if self.key[pg.K_DOWN] or self.key[pg.K_s]:
            self.acc.y = self.player_acc
        if self.key[pg.K_LEFT] or self.key[pg.K_a]:
            self.acc.x = -self.player_acc
        if self.key[pg.K_RIGHT] or self.key[pg.K_d]:
            self.acc.x = self.player_acc
        if self.key[pg.K_SPACE]:
            self._shot()

        super().update()

    def take_damage(self, amount, penetration=0):
        damage = amount
        if self.defense > penetration:
            damage = amount / (self.defense - penetration)

        self.health_points -= damage
        if self.health_points <= 0:
            self.kill()
