import pygame
from project.contants import FPS, HEIGHT, WIDTH


class Game:
    """
    Main Game class
    """
    def __init__(self):
        self.running = True
        self.playing = True

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.init()
        pygame.display.set_caption('Game in development')

    def new(self):
        """
        Every time a new game starts
        """
        self._run()

    def _run(self):

        while self.playing:
            self.clock.tick(FPS)
            self._events()
            self._update()
            self._draw()

    def _events(self):
        """
        Every event will be registered here
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = self.playing = False

    def _update(self):
        """
        Every sprite's update will be registered here
        """
        pass

    def _draw(self):
        """
        Everything we draw to the screen will be done here

        Don't forget that we always draw first then -> pygame.display.flip()
        """
        pass
