import pygame

from project.constants import Color, FPS, HEIGHT, WIDTH
from project.menus.home import Home
from project.sprites.fighter import Fighter
from project.sprites.player_character import PlayerCharacter
from project.sprites.structure import Structure


class Game:
    """
    Main Game class
    """

    def __init__(self):
        self.running = True
        self.playing = True

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.get_default_font()

        self.mouse_x = 0
        self.mouse_y = 0

        pygame.init()
        pygame.display.set_caption('Game in development')

    def new(self):
        """
        Every time a new game starts
        """
        self.all_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.player_character = PlayerCharacter(self, 15, 10, friction=3)

        # Testing enemies
        Structure(self, 100, 10, WIDTH - 500, pygame.Vector2(1, 1), pygame.Vector2(WIDTH, 500))
        Fighter(200, self, 100, 10, vel=pygame.Vector2(0, 0), pos=pygame.Vector2(WIDTH, 500), friction=4)

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
        key = pygame.key.get_pressed()

        if key[pygame.K_ESCAPE]:
            self.running = self.playing = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = self.playing = False

    def _update(self)-> None:
        """
        Every sprite's update will be registered here
        """
        self.all_sprites.update()

    def _draw(self)-> None:
        """
        Everything we draw to the screen will be done here

        Don't forget that we always draw first then -> pygame.display.flip()
        """
        self.screen.fill(Color.white)
        self.all_sprites.draw(self.screen)

        pygame.display.flip()

    def show_start_screen(self):

        self.screen.fill(Color.light_green)
        self.homepage = Home(self.screen)
        self.homepage.draw(self.mouse_x, self.mouse_y)
        self._wait_for_input()

    def _wait_for_input(self):
        waiting = True
        while waiting:
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            self.homepage.draw(self.mouse_x, self.mouse_y)

            self.clock.tick(FPS/2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = self.running = False
                if event.type == pygame.MOUSEBUTTONUP and self.homepage.play_button(self.mouse_x, self.mouse_y):
                    waiting = False
