import pygame

from project.constants import Color, HEIGHT, WIDTH


class Home:

    def __init__(self, screen: object):
        self.screen = screen

        # SCREEN: 1280x720px = WxH
        # devided by 5 parts horizontally - W/5 = 256px (slice)
        # devided by 8 parts vertically - H/8 = 90px (segment)

        self.slice = WIDTH // 5     # 256px
        self.segment = HEIGHT // 8  # 90px
        self.air = 10    # px
        self.shift = 20  # px
        self.space = 10  # px

        # LOGO: 768x360px
        # horizontal - logo takes 3 parts out of 5 - W/5 * 3 = 768px
        # vertical - logo takes half of H - H/2 = 360px
        self.logo_rect = pygame.Rect(self.slice, 0, self.slice * 3, HEIGHT / 2)
        self.logo_image = pygame.image.load("project/assets/images/logo_placeholder.png").convert_alpha()

        # PLAY BUTTON (larger) 384x70px
        # horizontal - one part and half of 5 = W/5 * 1.5 = 384px
        # vertical - 7 parts of 9 (of the segment) = S/9 * 7 = 70px
        # (10px for the air on top and the bottom)
        self.play_button_rect = pygame.Rect(self.space, self.segment * 4 + self.air,
                                            self.slice * 1.5,
                                            self.segment - (self.air * 2))

        # other buttons 320*70px
        # horizontal - one part and quarter of 5 = W/5 * 1.25 = 320px
        # vertical - 7 parts of 9 (of the segment) = S/9 * 7 = 70px
        # (10px for the air on top and the bottom)
        self.other_button_rect = pygame.Rect(self.space, self.segment * 5,
                                             self.slice * 1.25,
                                             self.segment - (self.air * 2))

        self.buttons_dict = {"options": 5, "about": 6, "exit": 7}

    def draw(self, x: int, y: int)-> None:

        self.screen.fill(Color.dark_blue)
        self.screen.blit(self.logo_image, self.logo_rect)

        self.play_button(x, y)
        for key in self.buttons_dict.keys():
            self._draw_other_buttons(x, y, key)
        pygame.display.update()

    def play_button(self, x: int, y: int)-> bool:

        self.play_button_rect.top = self.segment * 4
        self.play_button_rect.left = self.space
        hovered = self._hovered(x, y, self.play_button_rect)

        if hovered:
            self.play_button_rect.left = self.shift
            pygame.draw.rect(self.screen, Color.light_green, self.play_button_rect)
        else:
            self.play_button_rect.left = self.space
            pygame.draw.rect(self.screen, Color.light_green, self.play_button_rect)

        self._draw_text(50, "PLAY", Color.white, self.play_button_rect)

        return hovered

    def _draw_other_buttons(self, x: int, y: int, button: str)-> tuple:
        """
            Returns tuple of if it is hovored (bool) and the name of the button
        """

        self.other_button_rect.top = self.segment * self.buttons_dict[button]
        hovered = self._hovered(x, y, self.other_button_rect)

        if hovered:
            self.other_button_rect.left = self.shift
            pygame.draw.rect(self.screen, Color.light_green, self.other_button_rect)
        else:
            self.other_button_rect.left = self.space
            pygame.draw.rect(self.screen, Color.light_green, self.other_button_rect)

        self._draw_text(40, button.upper(), Color.white, self.other_button_rect)

        return hovered, button

    def _hovered(self, x: int, y: int, button: object)-> bool:
        return button.collidepoint(x, y)

    def _draw_text(self, size: int, text: str, color: Color, rect: pygame.Rect)->None:
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        text_surface = font.render(text, True, color)
        rect.top += self.air
        self.screen.blit(text_surface, rect)
