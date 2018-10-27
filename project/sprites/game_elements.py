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
    blasters = {'green': pg.image.load(str(PurePath(PATH_IMAGES).joinpath(PROJECTILE_IMAGE_NAME[0]))),
                'blue_marine': pg.image.load(str(PurePath(PATH_IMAGES).joinpath(PROJECTILE_IMAGE_NAME[1]))),
                'yellow': pg.image.load(str(PurePath(PATH_IMAGES).joinpath(PROJECTILE_IMAGE_NAME[2]))),
                'orange': pg.image.load(str(PurePath(PATH_IMAGES).joinpath(PROJECTILE_IMAGE_NAME[3]))),
                'red': pg.image.load(str(PurePath(PATH_IMAGES).joinpath(PROJECTILE_IMAGE_NAME[4]))),
                'purple': pg.image.load(str(PurePath(PATH_IMAGES).joinpath(PROJECTILE_IMAGE_NAME[5]))),
                'blue': pg.image.load(str(PurePath(PATH_IMAGES).joinpath(PROJECTILE_IMAGE_NAME[6])))
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
            self.image = Projectile.blasters['green']
        else:
            self.image = Projectile.blasters['blue_marine']

        self.image = pg.transform.scale(self.image, (round(self.owner.projectile_scale*100),
                                                     round(self.owner.projectile_scale*50)))
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

        # make own kill function

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
