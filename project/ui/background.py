from pathlib import PurePath

import pygame as pg
from pygame.image import load

from project.constants import PATH_IMAGES, WIDTH


class Background:

    def __init__(self, image_name: str, game, speed: int):
        self.game = game
        self.screen = game.screen
        self.game.nonsprite.add(self)
        self.image = load(str(PurePath(PATH_IMAGES).joinpath(image_name))).convert_alpha()
        self.x = 0
        self.x1 = WIDTH
        self.speed = speed

    def draw(self):

        self.x -= self.speed
        self.screen.blit(self.image, (self.x, 0))

        if abs(self.x) >= self.image.get_width() - WIDTH:
            self.screen.blit(self.image, (self.x1, 0))
            self.x1 -= self.speed
            if abs(self.x1) >= WIDTH:
                self.x = 0
                self.x1 = WIDTH
