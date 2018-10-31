import logging
import math
import random
from pathlib import PurePath

import pygame as pg

from project.constants import FIGHTER_IMAGE_NAME, HEIGHT, MINE_IMAGE_NAME, PATH_IMAGES, STRUCTURE_IMAGE_NAME, WIDTH
from project.sprites.fighter import Fighter
from project.sprites.mine import Mine
from project.sprites.structure import Structure

logger = logging.getLogger('last_judgment_logger')


class WaveGenerator:
    """Class responsible for spawning enemies"""

    def __init__(self, game):
        self.game = game
        self.game.nonsprite.add(self)
        self.difficulty = 1
        self.structure_image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(STRUCTURE_IMAGE_NAME)))
        self.fighter_image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(FIGHTER_IMAGE_NAME)))
        self.mine_image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(MINE_IMAGE_NAME)))

    def _generate(self, difficulty: int) -> None:
        for _ in range(math.floor(random.uniform(0, 0.25 * difficulty))):
            fighter = Fighter(
                self.game,
                -0.04,
                pg.Vector2(WIDTH, random.uniform(0, HEIGHT)),
                difficulty*50,
                10 + 2 * random.randint(0, difficulty),
                1+0.25*difficulty)
            logger.debug(f'Spawned a Fighter at {fighter.pos}')

        for _ in range(math.floor(random.uniform(1, math.sqrt(difficulty)))):
            structure = Structure(
                self.game,
                WIDTH - random.randint(50, 300),
                pg.Vector2(random.uniform(0.5, 2), 1),
                pg.Vector2(WIDTH, random.randint(75, HEIGHT - 75)),
                random.randint(2, max(2 + difficulty, 4*difficulty)),
                difficulty * 50)
            logger.debug(f'Spawned a Structure at {structure.pos}')

        for _ in range(math.floor(random.uniform(0, math.sqrt(0.25*difficulty)))):
            mine = Mine(
                self.game,
                pg.Vector2(random.uniform(0.5, 4), 0),
                pg.Vector2(WIDTH, random.uniform(200, HEIGHT - 200)),
                difficulty * 3,
                difficulty * 400
            )
            logger.debug(f'Spawned a Mine at {mine.pos}')

    def update(self) -> None:
        if len(self.game.enemy_sprites) == 0:
            self._generate(self.difficulty)
            logger.info(f'Wave {self.difficulty} started')
            self.difficulty += 1
