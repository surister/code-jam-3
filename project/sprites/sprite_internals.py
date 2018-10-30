import pygame as pg
from pygame.math import Vector2 as Vec

from project.constants import Color, MAX_SPEED


class Physics:
    """
    Sprite example

    class Character(Test, pygame.sprite.Sprite):
        def __init__(self, game):
            super().__init__()
            self.game = game
            self.add(self.game.all_sprites)
            self.image = pygame.Surface((50, 50))
            self.rect = self.image.get_rect()
            self.image.set_colorkey(Color.green)

            self.friction = 1
    """

    def __init__(self, friction: int = None):
        super().__init__()
        self.friction = 1 if friction is None else friction
        # Note that without friction (1), any object will move perpetually.

        self.acc = Vec(0, 0)
        self.vel = Vec(0, 0)
        self.pos = Vec()
        self.max_speed = MAX_SPEED

    def update(self):
        if self.friction > 1:  # dev stuff, TODO delete on final product
            print('friction should be negative and really small eg; -0.05.')

        # Friction
        self.acc += self.vel * self.friction

        # Basic motion
        self.vel += self.acc

        if self.vel.x > self.max_speed:
            self.vel.x = self.max_speed
        if self.vel.y > self.max_speed:
            self.vel.y = self.max_speed
        if self.vel.x < -self.max_speed:
            self.vel.x = -self.max_speed
        if self.vel.y < -self.max_speed:
            self.vel.y = -self.max_speed

        self.pos += self.vel + 0.5 * self.acc  # plus something, friction?

        self.rect.center = self.pos


class TestingCharacter(Physics, pg.sprite.Sprite):
    """
    Sprite made for the sake of testing.
    """

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.add(self.game.all_sprites)
        self.image = pg.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(Color.green)
