from collections import deque
from typing import Union


import pygame as pg

from project.constants import Color, FIRE_RATE, PLAYER_ACC
from project.sprites.combat import Combat
from project.sprites.sprite_internals import Physics
from project.ui.character_interface import StaticHealthbar


class Character(Combat, Physics, pg.sprite.Sprite):
    """ Base class for Character, current implementation based on dev_character """

    def __init__(
        self,
        game,
        health: int,
        defence: int,
        shield: int = 50,
        pos: pg.Vector2 = None,
        acc: pg.Vector2 = None,
        vel: pg.Vector2 = None,
        weapons: list = None,
        friction: Union[int, float] = 1,
        image: pg.Surface = None
    ):

        Physics.__init__(self, friction)
        Combat.__init__(self, health, defence, shield=shield)

        super().__init__(health, defence)

        self.game = game
        self.add(self.game.all_sprites)

        self.player_acc = PLAYER_ACC
        self.fire_rate = FIRE_RATE
        self.health = health
        self.shield = shield
        self.defense = defence
        self.projectiles = deque()
        self.evil = False
        self.type = 1

        self.rapid_fire = True
        if self.rapid_fire:
            self.fire_rate -= 20

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

        self.healthbar = StaticHealthbar(self.game, self, 70, 40)
        self.mask = pg.mask.from_surface(self.image)

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
            # self._take_damage(10)

        super().update()
