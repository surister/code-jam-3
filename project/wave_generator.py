import random
import math
from pathlib import PurePath

import pygame as pg

from project.constants import PATH_IMAGES, STRUCTURE_IMAGE_NAME, FIGHTER_IMAGE_NAME, MINE_IMAGE_NAME, WIDTH, HEIGHT
from project.sprites.fighter import Fighter
from project.sprites.mine import Mine
from project.sprites.structure import Structure


class WaveGenerator:
    """Class responsible for spawning enemies"""
    def __init__(self, game: 'Game'):
        self.game = game
        self.difficulty = 1
        self.wave_group = pg.sprite.Group()

        self.structure_image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(STRUCTURE_IMAGE_NAME)))
        self.fighter_image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(FIGHTER_IMAGE_NAME)))
        self.mine_image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(MINE_IMAGE_NAME)))

    def _generate(self, difficulty: int) -> None:
        for _ in range(math.floor(random.uniform(0, 0.25* difficulty))):
            self.wave_group.add(Fighter(self.game, -0.04, pg.Vector2(WIDTH, random.uniform(0, HEIGHT)), difficulty*50, 10 + 2 * random.randint(0, difficulty), 1+0.25*difficulty))

        for _ in range(math.floor(random.uniform(1, math.sqrt(difficulty)))):
            self.wave_group.add(Structure(self.game, WIDTH - random.randint(50, 300), pg.Vector2(random.uniform(0.5, 2), 1), pg.Vector2(WIDTH, random.randint(20, HEIGHT)), difficulty * 50))


    def update(self) -> None:
        if len(self.wave_group) == 0:
            print(f"Wave {self.difficulty} started")
            self._generate(self.difficulty)
            self.difficulty += 1