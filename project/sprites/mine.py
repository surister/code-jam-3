from pathlib import PurePath

import pygame as pg

from project.ui.sheet import Sheet
from project.constants import Color, MINE_IMAGE_NAME, PATH_IMAGES
from project.sprites.combat import Combat


class Mine(Combat, pg.sprite.Sprite):
    """
    Represents a Mine that slowly move to the asteroid, exploding on impact of asteroid or player.
    """
    path = str(PurePath(PATH_IMAGES).joinpath(MINE_IMAGE_NAME))

    def __init__(
        self,
        game,
        vel: pg.Vector2,
        pos: pg.Vector2,
        health: int=15,
        points: int=150
    ):
        Combat.__init__(self, health, points=points)
        pg.sprite.Sprite.__init__(self)

        self.game = game
        self.vel = vel
        self.pos = pos
        self.attack = 3
        self.timer = 0
        self.current_frame = 0
        self.frames = [pg.transform.scale(Sheet(Mine.path).get_image(0, 0, 250, 250, alpha=True), (100, 100)),
                       pg.transform.scale(Sheet(Mine.path).get_image(250, 0, 250, 250, alpha=True), (100, 100))]

        self.image = self.frames[0]
        self.rect = self.image.get_rect()

        self.add(self.game.all_sprites, self.game.mines)

        self.image.set_colorkey(Color.black)

        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        """
        Overrides pg.sprite.Sprite update function and gets called in /game.py/Game class

        Move left untill off screen
        """
        now = pg.time.get_ticks()
        if now - self.timer > 500:
            self.timer = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.image = self.frames[self.current_frame]

        self.pos.x = self.pos.x - self.vel.x
        if self.pos.x < 0:
            self.kill()
        self.rect.midbottom = self.pos

        super().update()
