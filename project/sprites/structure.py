import pygame as pg

from project.constants import Color


class Structure(pg.sprite.Sprite):
    """ Structures slow move from off screen to their fixed position and then start firing at the player. """

    def __init__(
        self,
        game,
        destination: int,
        vel,
        pos,
        image: pg.Surface= None
    ):
        super().__init__()
        self.destination = destination
        self.arrived = False
        self.game = game
        self.vel = vel
        self.pos = pos

        if image is None:
            self.image = pg.Surface((80, 80))
            self.image.fill(Color.red)
        else:
            self.image = image
        self.rect = self.image.get_rect()

        self.add(self.game.all_sprites)
        self.add(self.game.enemy_sprites)

        self.image.set_colorkey(Color.black)

    def update(self):
        """ Move left untill destination passed if not already there, otherwise shoot at the player """
        if not self.arrived:
            self.pos.x = self.pos.x - self.vel.x

            if self.pos.x < self.destination:
                self.arrived = True
        else:
            # TODO implement once projectiles are added to the game
            pass
        self.rect.midbottom = self.pos
        super().update()
