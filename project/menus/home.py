import pygame
from project.constants import Color, HEIGHT, WIDTH


class Home:

    def __init__(self, screen: object):
        self.screen = screen
        self.start_button = pygame.Rect(0, 0, 400, 100)
        self.start_button.midtop = (WIDTH/2, HEIGHT/7)
        self.start_button_text = "START"

    def draw(self, x: int, y: int):
        self.screen.fill(Color.dark_blue)

        in_horizontal = x > self.start_button.left and x < self.start_button.left + self.start_button.width
        in_vertical = y > self.start_button.top and y < self.start_button.top + self.start_button.height

        if in_horizontal and in_vertical:
            self._draw_start_button(hover=True)
        else:
            self._draw_start_button()

    def _draw_start_button(self, hover=False)->None:

        color = Color.dark_yellow

        if hover:
            color = Color.red

        font = pygame.font.Font(pygame.font.get_default_font(), 60)
        text_surface = font.render(self.start_button_text, True, Color.white)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH/2, HEIGHT/7)
        text_rect.top += 20

        pygame.draw.rect(self.screen, color, self.start_button)
        self.screen.blit(text_surface, text_rect)
