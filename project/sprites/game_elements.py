import pygame as pg

from project.sprites.physics import Physics
from project.constants import Color


class Projectile(Physics, pg.sprite.Sprite):
    def __init__(self, game, player):
        super().__init__()
        self.game = game
        self.player = player
        self.add(self.game.all_sprites, self.game.others)

        self.damage: int = 2
        self.image = pg.Surface((15, 15))
        self.rect = self.image.get_rect()
        self.image.fill(Color.dark_blue)

    def update(self):
        self.rect.midbottom = self.player.pos

        self.acc.x = 10
