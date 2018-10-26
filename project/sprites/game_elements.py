import math

import pygame as pg

from project.constants import Color, HEIGHT, WIDTH
from project.sprites.sprite_internals import Physics


class Projectile(Physics, pg.sprite.Sprite):
    """Basic Projectile Sprite"""
    def __init__(self, game, owner, angle: float, damage: int=2, penetration: int=0, spawn_point=None, image=None):
        super().__init__()
        self.game = game
        self.owner = owner

        if owner.evil:
            self.add(self.game.all_sprites, self.game.enemy_projectiles)
        else:
            self.add(self.game.all_sprites, self.game.others)

        self.angle = angle
        self.damage = damage
        self.penetration = penetration

        if image is None:
            self.image = pg.Surface((15, 15))
            self.image.fill(Color.green)
        else:
            self.image = image

        self.image = pg.transform.rotate(self.image, angle * 180 / math.pi)

        if spawn_point is None:
            self.pos = owner.rect.midright
        else:
            self.pos = spawn_point

        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        # TODO BULLET LIFE TIME
        self.friction = 0.012
        super().update()

        self.vel.y = -10 * math.sin(self.angle)
        self.vel.x = 10 * math.cos(self.angle)

        self.max_speed = 20

        if self.pos.y > HEIGHT:
            self.kill()
            self.owner.projectiles.pop()
        if self.pos.y < 0:
            self.kill()
            self.owner.projectiles.pop()
        if self.pos.x > WIDTH:
            self.kill()
            self.owner.projectiles.pop()
        if self.pos.x < 0:
            self.kill()
            self.owner.projectiles.pop()


class Item(pg.sprite.Sprite):
    """Represents items such as drops"""
    pass
