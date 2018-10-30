import math
import random
from pathlib import PurePath

import pygame as pg

from project.constants import Color, HEIGHT, PATH_IMAGES, POWERUPS, POWERUP_EFFECT, PROJECTILE_IMAGE_NAME, WIDTH
from project.sprites.sprite_internals import Physics
from project.ui.sheet import Sheet
from project.ui.timer import Timer


class Projectile(Physics, pg.sprite.Sprite):
    """Basic Projectile Sprite

    Blaster 0 -> Green
    Blaster 1 -> Blue_marine
    Blaster 2 -> Yellow
    Blaster 3 -> Orange
    Blaster 4 -> Red
    Blaster 5 -> Purple  For double shots
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
        if self.owner.type == 5:
            self.image = Projectile.blasters['purple']
        else:
            self.image = Projectile.blasters['blue_marine']

        self.image = pg.transform.scale(self.image, (round(self.owner.projectile_scale*90),
                                                     round(self.owner.projectile_scale*40)))
        self.image = pg.transform.rotate(self.image, angle * 180 / math.pi)
        if spawn_point is None:
            self.pos = owner.rect.midright
        else:
            self.pos = spawn_point

        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pg.mask.from_surface(self.image)

    def destroy(self):
        # TODO FIX THIS BUG

        self.kill()
        try:
            self.owner.projectiles.remove(self)
        except ValueError:
            pass

    def update(self):
        self.friction = 0.012
        super().update()

        self.vel.y = -10 * math.sin(self.angle)
        self.vel.x = 10 * math.cos(self.angle)

        self.max_speed = 20

        # make own kill function
        if self.pos.y > HEIGHT:
            self.destroy()
        if self.pos.y < 0:
            self.destroy()
        if self.pos.x > WIDTH:
            self.destroy()
        if self.pos.x < 0:
            self.destroy()


class Item(pg.sprite.Sprite):
    """Represents items such as drops
    red: + soft hp
    pink: + full hp
    purple: temporary double shot x seconds
    blue: + max shield
    yellow: temporary immunity
    white: temporary extra fire rate
    green: + armor
    white: permanent extra damage
    """
    def __init__(self, game, color: str = None):
        super().__init__()
        self.game = game
        self.color = color
        self.add(self.game.all_sprites, self.game.powerups)

        self.color_location = {'red': (0, 0, 130, 130),
                               'pink': (129, 0, 130, 130),
                               'purple': (255, 0, 130, 130),
                               'blue': (385, 0, 130, 130),
                               'yellow': (0, 130, 130, 130),
                               'white': (129, 130, 130, 130),
                               'green': (255, 130, 130, 130),
                               'w_green': (385, 130, 130, 130)
                               }
        if self.color is None:
            self.type = random.choice(['red', 'pink', 'purple', 'blue', 'yellow', 'white', 'green', 'w_green'])
        else:
            self.type = self.color

        self.image = Sheet(str(PurePath(PATH_IMAGES).joinpath(POWERUPS))).get_image(*self.color_location[self.type])
        self.image.set_colorkey(Color.black)
        self.image = pg.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()

        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = (random.randint(200, 700), random.randint(200, 700))

    def apply_powerup(self, character: pg.sprite.Sprite):
        if self.type in ['purple', 'yellow', 'white']:

            Timer(self.game, POWERUP_EFFECT[self.type], 15, 20, pg.font.get_default_font(), 40)
        if self.type == 'red':
            character.heal(POWERUP_EFFECT[self.type])
        if self.type == 'pink':
            character.heal(POWERUP_EFFECT[self.type])
        if self.type == 'purple':
            character.double_shot(POWERUP_EFFECT[self.type])
        if self.type == 'blue':
            character.heal_shield()
        if self.type == 'yellow':
            character.immune(POWERUP_EFFECT[self.type])
        if self.type == 'white':
            character.fast_fire(POWERUP_EFFECT[self.type])
        if self.type == 'green':
            character.armor += POWERUP_EFFECT[self.type]
        if self.type == 'w_green':
            character.attack += POWERUP_EFFECT[self.type]
