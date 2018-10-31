from collections import deque
from pathlib import PurePath
from typing import Union


import pygame as pg

from project.constants import CHARACTER_SPACESHIP, Color, FIRE_RATE, PATH_IMAGES, PLAYER_ACC
from project.sprites.combat import Combat
from project.sprites.sprite_internals import Physics
from project.ui.character_interface import StaticHealthbar
from project.ui.sheet import Sheet


class Character(Combat, Physics, pg.sprite.Sprite):
    """ Main Character Class """
    path = str(PurePath(PATH_IMAGES).joinpath(CHARACTER_SPACESHIP))

    def __init__(
        self,
        game,
        health: int,
        defence: int,
        shield: int = 50,
        pos: pg.Vector2 = None,
        acc: pg.Vector2 = None,
        vel: pg.Vector2 = None,
        friction: Union[int, float] = 1
    ):

        Physics.__init__(self, friction)
        Combat.__init__(self, health, defence, shield=shield)

        super().__init__(health, defence)

        self.game = game
        self.add(self.game.all_sprites)

        self.image_code = 1
        self.images = {1: pg.transform.scale(Sheet(Character.path).
                                        get_image(200, 460, 310, 300, alpha=True), (60, 60)),    # red
                       2: pg.transform.scale(Sheet(Character.path).
                                        get_image(200, 760, 310, 300, alpha=True), (60, 60)),    # blue
                       3: pg.transform.scale(Sheet(Character.path).
                                        get_image(200, 1060, 310, 300, alpha=True), (60, 60)),    # green
                       4: pg.transform.scale(Sheet(Character.path).
                                        get_image(600, 760, 310, 300, alpha=True), (60, 60)),    # yellow
                       5: pg.transform.scale(Sheet(Character.path).
                                        get_image(600, 1060, 310, 300, alpha=True), (60, 60)),   # orange
                       6: pg.transform.scale(Sheet(Character.path).
                                        get_image(900, 760, 310, 300, alpha=True), (60, 60)),    # purple
                       7: pg.transform.scale(Sheet(Character.path).
                                        get_image(900, 1060, 310, 300, alpha=True), (60, 60)),   # pink
                       8: pg.transform.scale(Sheet(Character.path).
                                        get_image(1250, 1060, 310, 300, alpha=True), (60, 60))  # black
                       }

        self.image = self.images[1]
        self.image.set_colorkey(Color.black)

        self.player_acc = PLAYER_ACC
        self.fire_rate = FIRE_RATE
        self.health = health
        self.shield = shield
        self.defense = defence
        self.projectiles = deque()
        self.type = 1

        self.fire_rate -= 20
        self.evil = False
        self.check_for_double_shot = False
        self.check_for_immunity = False
        self.check_for_rapid_fire = False
        self.time_update = 0

        if self.rapid_fire:
            self.fire_rate -= 100
        self.rect = self.image.get_rect()

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

    def heal(self, amount: int)-> None:
        """
        Heals :param amount

        If the amount + current heal is larger than max_health then current health is
        max_health, healing the character to its maximum and ignoring amount
        """
        if self.health + amount > self.max_health:
            self.health = self.max_health
        else:
            self.health += amount

    def heal_shield(self)-> None:
        """
        Shield is set to max

        """
        self.shield = self.max_health / 2

    def double_shot(self, duration: int)-> None:
        """
        During :param duration seconds the character shots two projectiles instead of one.
        """
        self.double_shot_time = pg.time.get_ticks()
        self.type = 5
        self.double_s = True
        self.double_shot_duration = duration
        self.check_for_double_shot = True

    def immune(self, duration: int)-> None:
        """
        During :param duration: seconds the character cannot receive any damage
        """
        self.immune_time = pg.time.get_ticks()
        self.immunity_duration = duration
        self.immunity = True
        self.check_for_immunity = True

    def fast_fire(self, duration: int)-> None:
        """
        During :param duration: seconds the character rapid_fire decreases (incrementing character
        fire speed
        """

        self.fast_time = pg.time.get_ticks()
        self.rapid_fire_duration = duration
        self.rapid_fire = True
        self.check_for_rapid_fire = True
        self.fire_rate -= 40

    def update(self) -> None:
        """
        Overrides pg.sprite.Sprite update function and gets called in /game.py/Game class

        Depending on the check flags we check for boosts duration.
        Key -> movement is also done here.
        """

        self.image = self.images[self.image_code]

        if self.check_for_double_shot:
            now = pg.time.get_ticks()
            if now > self.double_shot_time + self.double_shot_duration * 1000:
                self.time_update = now
                self.double_s = False
                self.type = 1
                self.check_for_double_shot = False

        if self.check_for_immunity:
            now = pg.time.get_ticks()
            if now > self.immune_time + self.immunity_duration * 1000:
                self.time_update = now
                self.immunity = False
                self.check_for_immunity = False

        if self.check_for_rapid_fire:
            now = pg.time.get_ticks()
            if now > self.fast_time + self.rapid_fire_duration * 1000:
                self.time_update = now
                self.immunity = False
                self.check_for_rapid_fire = False
                self.fire_rate += 40

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
