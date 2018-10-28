from pathlib import PurePath

import pygame as pg

from project.constants import CHARACTER_IMAGE_NAME, DATA, FPS, HEIGHT, PATH_IMAGES, WIDTH
from project.sprites.character import Character
from project.sprites.fighter import Fighter
from project.sprites.mine import Mine
from project.sprites.structure import Structure
from project.ui.background import Background
from project.ui.intro import Intro
from project.ui.main_menu import Home
from project.ui.timer import Timer


class CustomGroup:
    def __init__(self):
        self.elements = []

    def __len__(self):
        return len(self.elements)

    def __repr__(self):
        return f'{self.elements}'

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
        self.pause = True

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.font = pg.font.get_default_font()

        self.mouse_x = 0
        self.mouse_y = 0

        self.score = 0

        pg.init()
        pg.mixer.init()
        pg.display.set_caption('Game in development')
        pg.mouse.set_cursor((8, 8), (0, 0), ((0,) * 8), ((0,) * 8))

        self.pause_background = pg.image.load(str(PurePath(PATH_IMAGES).joinpath("background3.png"))).\
            convert_alpha()

    def new(self):
        """
        Every time a new game starts
        """

        self.all_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
        self.others = pg.sprite.Group()  # Find a better name? Projectiles will be stored here for now

        self.nonsprite = CustomGroup()

        self.enemy_projectiles = pg.sprite.Group()

        # Testing enemies
        self.background = Background("stars2.png", self, 5)

        Structure(self, WIDTH - 250, pg.Vector2(1, 1), pg.Vector2(WIDTH, 500))

        Fighter(self, 200, vel=pg.Vector2(0, 0), pos=pg.Vector2(WIDTH, 500), friction=-0.02)

        Mine(self, pg.Vector2(1.5, 1.5), pg.Vector2(WIDTH, 200))

        char_image = pg.image.load(str(PurePath(PATH_IMAGES).joinpath(CHARACTER_IMAGE_NAME)))
        self.devchar = Character(self, 100, 10, friction=-0.052, image=char_image, shield=50)

        self.timer = Timer(self, 600, WIDTH // 2 - 70, 25, "Ariel", 80)

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
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = self.playing = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self._pause()

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

        enemy_projectiles = pg.sprite.spritecollide(self.devchar, self.enemy_projectiles, False)
        for projectile in enemy_projectiles:
            self.devchar.damage(projectile)
            projectile.kill()

    def _draw(self)-> None:
        """
        Everything we draw to the screen will be done here

        Don't forget that we always draw first then -> pg.display.flip()
        """
        self.nonsprite.draw()
        self.all_sprites.draw(self.screen)

        pg.display.flip()

    def _destroy(self):
        self.kill()
        # TODO show end screen

    def play_intro(self):

        if DATA["intro_played"]:
            return
        else:
            intro = Intro(self.screen)

            while intro.playing:
                intro.play()
                self.clock.tick(FPS/2)

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        intro.playing = self.running = False

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

    def _pause(self):

        waiting = True
        while waiting:
            self.screen.blit(self.pause_background, (0, 0))
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        waiting = False
