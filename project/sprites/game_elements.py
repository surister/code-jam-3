import pygame as pg

from project.constants import Color
from project.sprites.physics import Physics


class Projectile(Physics, pg.sprite.Sprite):
    def __init__(self, game, player):
        super().__init__()
        self.game = game
        self.player = player
        self.add(self.game.all_sprites, self.game.others)

        self.damage: int = 2
        self.image = pg.Surface((15, 15))
        self.rect = self.image.get_rect()
        self.image.fill(Color.green)
        self.first_pos = self.player.pos
        self.rect.midbottom = self.first_pos

    def update(self):
        super().update()
        self.acc.x = 1
        self.max_speed = 20
