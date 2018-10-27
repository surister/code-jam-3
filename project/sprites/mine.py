import pygame as pg

from project.constants import Color
from project.sprites.combat import Combat
from project.ui.character_interface import MovableHealtbar


class Mine(Combat, pg.sprite.Sprite):
    """ Mines slowly move to the asteroid, exploding on impact of asteroid or player. """

    def __init__(
        self,
        game,
        vel,
        pos,
        points: int=150,
        image: pg.Surface= None
    ):
        Combat.__init__(self, 30, points=points)
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.vel = vel
        self.pos = pos

        if image is None:
            self.image = pg.Surface((60, 60))
            self.image.fill(Color.red)
        else:
            self.image = image
        self.rect = self.image.get_rect()

        self.add(self.game.all_sprites, self.game.enemy_sprites)

        self.image.set_colorkey(Color.black)
        #self.healthbar = MovableHealtbar(self.game, self, self.pos.x, self.pos.y)

    def update(self):
        """ Move left untill off screen """
        self.pos.x = self.pos.x - self.vel.x
        if self.pos.x < 0:
            self.kill()
        self.rect.midbottom = self.pos

        # self.healthbar = Healthbar(game=self.game, owner=self, x=self.pos.x - 500, y=self.pos.y)

        super().update()
