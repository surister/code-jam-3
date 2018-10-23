import pygame

from project.constants import Color, HEIGHT, WIDTH


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

            self.acc = pygame.Vector2(0, 0)
            self.vel = pygame.Vector2(0, 0)
            self.pos = pygame.Vector2(200, 200)

            self.friction = 1
    """

    def __init__(self, friction):
        super().__init__()
        self.friction = 0.1

    def update(self) -> None:

        # self.acc += self.vel * self.friction

        self.vel += self.acc * self.friction

        if self.vel.x > 10:
            self.vel.x = 10
        if self.vel.y > 10:
            self.vel.y = 10
        if self.vel.x < -10:
            self.vel.x = -10
        if self.vel.y < -10:
            self.vel.y = -10

        self.pos += self.vel  # plus something, friction?

        self.rect.midbottom = self.pos

        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH


class Character(Physics, pygame.sprite.Sprite):
    """
    Sprite made for the sake of testing.
    """

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.add(self.game.all_sprites)
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(Color.green)

        self.acc = pygame.Vector2(0, 0)
        self.vel = pygame.Vector2(0, 0)
        self.pos = pygame.Vector2(200, 200)

        self.friction = 1