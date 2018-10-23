import pygame

from project.constants import Color, FPS, HEIGHT, WIDTH
from project.menus.home import Home
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
        self.player_character = PlayerCharacter(self, 15, 10)

        """ test enemies """
        Structure(self, 100, 10, WIDTH - 500, pygame.Vector2(1, 1), pygame.Vector2(WIDTH, 500))

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

            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

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

        homepage = Home(self.screen)
        homepage.draw(self.mouse_x, self.mouse_y)
        # self.screen.fill(Color.white)
        self.all_sprites.draw(self.screen)

        pygame.display.flip()

    def _draw_text(self, size: int, text: str, color: Color, cords: tuple):
        font = pygame.font.Font(self.font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = cords
        self.screen.blit(text_surface, text_rect)
