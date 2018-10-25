import pygame as pg

from project.constants import Color, HEIGHT, WIDTH
from project.sprites.physics import Physics


class Projectile(Physics, pg.sprite.Sprite):
    """Basic Projectile Sprite"""
    def __init__(self, game, owner, direction: int=None, image=None):
        super().__init__()
        self.game = game
        self.owner = owner
        self.add(self.game.all_sprites, self.game.others)

        if direction not in (1, -1):
            print('Direction should be only to mark negative or positive direction.')
        self.direction = direction
        self.damage: int = 2

        if image is None:
            self.image = pg.Surface((15, 15))
            self.image.fill(Color.green)
        else:
            self.image = image

        self.pos = pg.Vector2(owner.rect.midright)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        # TODO BULLET LIFE TIME
        self.friction = 0.012
        super().update()
        self.vel.x = 10 * self.direction

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
