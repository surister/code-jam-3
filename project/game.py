from pathlib import PurePath

import pygame as pg

from project.constants import CHARACTER_IMAGE_NAME, FIGHTER_IMAGE_NAME, FPS, \
    HEIGHT, MINE_IMAGE_NAME, PATH_IMAGES, STRUCTURE_IMAGE_NAME, WIDTH
from project.sprites.character import Character
from project.sprites.fighter import Fighter
from project.sprites.mine import Mine
from project.sprites.structure import Structure
from project.ui.background import Background
from project.ui.character_interface import Healthbar
from project.ui.main_menu import Home


class CustomGroup:
    def __init__(self):
        self.elements = []

    def add(self, element):
        if hasattr(element, 'draw'):
            self.elements.append(element)
        else:
            raise AttributeError(f'{element.__class__.__name__} has no attribute draw')

    def draw(self):
        for element in self.elements:
            element.draw()


class Game:
    """
    Main Game class
    """

    def __init__(self):
        self.running = True
        self.playing = True

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.font = pg.font.get_default_font()


        self.mouse_x = 0
        self.mouse_y = 0

        pg.init()
        pg.display.set_caption('Game in development')
        pg.mouse.set_cursor((8, 8), (0, 0), ((0,) * 8), ((0,) * 8))

    def new(self):
        """
        Every time a new game starts
        """

        self.all_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
        self.others = pg.sprite.Group()  # Find a better name? Projectiles will be stored here for now
        self.nonsprite = CustomGroup()
        # Testing enemies
        self.background = Background("stars2.png", self, 5)
        structure_image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(STRUCTURE_IMAGE_NAME)))
        Structure(self, WIDTH - 250, pg.Vector2(1, 1), pg.Vector2(WIDTH, 500), image=structure_image)

        fighter_image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(FIGHTER_IMAGE_NAME)))
        Fighter(self, 200, vel=pg.Vector2(0, 0), pos=pg.Vector2(WIDTH, 500), friction=-0.06, image=fighter_image)

        mine_image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(MINE_IMAGE_NAME)))
        Mine(self, pg.Vector2(0.5, 0.5), pg.Vector2(WIDTH, 200), image=mine_image)

        char_image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(CHARACTER_IMAGE_NAME)))
        self.devchar = Character(self, 100, 10, friction=-0.052, image=char_image, shield=50)
        self.healthbar = Healthbar(self, self.devchar, self.screen, 100, 200, 200)
        # TODO WITH SPREADSHEET IMAGE LOAD WON'T BE HERE, BUT IN EVERY SPRITE CLASS
        self._run()

    def _run(self)-> None:

        while self.playing:
            self.clock.tick(FPS)
            self._events()
            self._update()
            self._draw()

    def _events(self)-> None:
        """
        Every event will be registered here
        """
        key = pg.key.get_pressed()

        if key[pg.K_ESCAPE]:
            self.running = self.playing = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = self.playing = False

    def _update(self)-> None:
        """
        Every sprite's update will be registered here
        """
        self.all_sprites.update()

        """# collide projectiles with enemies
        for projectile in self.devchar.projectiles:
            for enemy in self.enemy_sprites:
                if projectile.collideswith(enemy):
                    enemy.damage(projectile)
        """

        for enemy in self.enemy_sprites:
            projectiles = pg.sprite.spritecollide(enemy, self.others, False)
            for projectile in projectiles:
                enemy.damage(projectile)
                projectile.kill()

    def _draw(self)-> None:
        """
        Everything we draw to the screen will be done here

        Don't forget that we always draw first then -> pg.display.flip()
        """


        self.nonsprite.draw()
        self.healthbar.draw(self.devchar.health, self.devchar.shield)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):

        self.homepage = Home(self.screen)
        self._wait_for_input()

    def _wait_for_input(self):
        waiting = True
        while waiting:
            self.mouse_x, self.mouse_y = pg.mouse.get_pos()
            self.homepage.draw(self.mouse_x, self.mouse_y)

            self.clock.tick(FPS/2)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = self.running = False
                if event.type == pg.MOUSEBUTTONUP and self.homepage.buttons_hover_states["play"]:
                    waiting = False
                if event.type == pg.MOUSEBUTTONUP and self.homepage.buttons_hover_states["gitlab"]:
                    self.homepage.open_gitlab()
                if event.type == pg.MOUSEBUTTONUP and self.homepage.buttons_hover_states["exit"]:
                    self.running = self.playing = waiting = False
