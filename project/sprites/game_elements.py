import math
from pathlib import PurePath

import pygame as pg

from project.constants import HEIGHT, PATH_IMAGES, PROJECTILE_IMAGE_NAME, WIDTH
from project.sprites.sprite_internals import Physics


class Projectile(Physics, pg.sprite.Sprite):
    """Basic Projectile Sprite

    Blaster 0 -> Green
    Blaster 1 -> Blue_marine
    Blaster 2 -> Yellow
    Blaster 3 -> Orange
    Blaster 4 -> Red
    Blaster 5 -> Purple
    Blaster 6 -> Blue
    """
    blasters = {0: pg.image.load(str(PurePath(PATH_IMAGES).joinpath(PROJECTILE_IMAGE_NAME[0]))),
                1: pg.image.load(str(PurePath(PATH_IMAGES).joinpath(PROJECTILE_IMAGE_NAME[1]))),
                2: pg.image.load(str(PurePath(PATH_IMAGES).joinpath(PROJECTILE_IMAGE_NAME[2]))),
                3: pg.image.load(str(PurePath(PATH_IMAGES).joinpath(PROJECTILE_IMAGE_NAME[3]))),
                4: pg.image.load(str(PurePath(PATH_IMAGES).joinpath(PROJECTILE_IMAGE_NAME[4]))),
                5: pg.image.load(str(PurePath(PATH_IMAGES).joinpath(PROJECTILE_IMAGE_NAME[5])))
                }

    def __init__(self, game, owner, angle: float, damage: int=2, penetration: int=0, spawn_point=None):
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

        if self.owner.type == 1:
            self.image = Projectile.blasters[0]
        else:
            self.image = Projectile.blasters[1]
        self.image = pg.transform.scale(self.image, (100, 50))
        self.image = pg.transform.rotate(self.image, angle * 180 / math.pi)
        if spawn_point is None:
            self.pos = owner.rect.midright
        else:
            self.pos = spawn_point

        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
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
