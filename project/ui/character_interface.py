import pygame as pg

from project.constants import Color


class Healthbar:

    def __init__(self, game, owner, x: int, y: int, width=None):
        super().__init__()
        self.game = game
        self.owner = owner
        self.screen = self.game.screen

        self.x = x
        self.y = y
        self.width = width
        self.game.nonsprite.add(self)

    def draw(self) -> None:

        self.hp = self.owner.health
        self.sp = self.owner.shield

        hp_color = Color.pure_green
        sp_color = Color.pure_blue
        if self.hp <= 0:
            self.hp = 0

        if self.hp < 40:
            hp_color = Color.red
        pg.draw.rect(self.screen, hp_color, [70, 50, self.hp*2, 20])

        if self.sp is not None:
            pg.draw.rect(self.screen, sp_color, [70, 80, self.sp*2, 20])


class MovableHealtbar(pg.sprite.Sprite):

    def __init__(self, game, owner, x: int, y: int):
        super().__init__()
        self.game = game
        self.add(self.game.all_sprites)
        self.owner = owner
        self.screen = self.game.screen
        self.image = pg.Surface((100, 20))
        self.image.fill(Color.red)
        self.rect = self.image.get_rect()

        self.pos = (x, y)

    def update(self):
        self.image = pg.Surface((100, 20))
        self.rect.midbottom = self.owner.pos
        self.game.screen.blit(self.image, self.rect)
