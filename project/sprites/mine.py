import pygame as pg

from project.constants import Color
from project.sprites.combat import Combat
from project.ui.character_interface import Healthbar


class Mine(Combat, pg.sprite.Sprite):
    """ Mines slowly move to the astroid, exploding on impact of asteroid or player. """

    def __init__(
        self,
        game,
        vel,
        pos,
        image: pg.Surface= None
    ):
        Combat.__init__(self, 30)
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

        self.add(self.game.all_sprites)
        self.add(self.game.enemy_sprites)

        self.image.set_colorkey(Color.black)

    def update(self):
        """ Move left untill off screen """
        self.pos.x = self.pos.x - self.vel.x
        if self.pos.x < 0:
            self.kill()
        self.rect.midbottom = self.pos

        self.healthbar = Healthbar(self.game, self, self.game.screen, self.pos.x - 500, self.pos.y)

        super().update()
