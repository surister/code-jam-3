import pygame as pg

from project.constants import Color, FPS, HEIGHT, WIDTH
from project.menus.home import Home
from project.sprites.character import Character
from project.sprites.fighter import Fighter
from project.sprites.structure import Structure


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

    def new(self):
        """
        Every time a new game starts
        """
        self.all_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()

        # Testing enemies
        Structure(self, WIDTH - 250, pg.Vector2(1, 1), pg.Vector2(WIDTH, 500))
        Fighter(self, 200, vel=pg.Vector2(0, 0), pos=pg.Vector2(WIDTH, 500), friction=-0.06)

        self.others = pg.sprite.Group()  # Find a better name? Projectiles will be stored here for now
        self.devchar = Character(self, 10, 10, friction=-0.052)

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

    def _draw(self)-> None:
        """
        Everything we draw to the screen will be done here

        Don't forget that we always draw first then -> pg.display.flip()
        """
        self.screen.fill(Color.white)
        self.all_sprites.draw(self.screen)

        pg.display.flip()

    def show_start_screen(self):

        self.screen.fill(Color.light_green)
        self.homepage = Home(self.screen)
        self.homepage.draw(self.mouse_x, self.mouse_y)
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
                if event.type == pg.MOUSEBUTTONUP and self.homepage.play_button(self.mouse_x, self.mouse_y):
                    waiting = False
