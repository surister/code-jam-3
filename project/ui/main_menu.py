import webbrowser as wb
from pathlib import PurePath

import pygame
from pygame.image import load

from project.constants import Color, GIT_LAB_LINK, HEIGHT, PATH_IMAGES, WIDTH


class Home:

    def __init__(self, screen):
        self.screen = screen

        # SCREEN: 1280x720px = WxH
        # devided by 5 parts horizontally - W/5 = 256px (slice)
        # devided by 8 parts vertically - H/8 = 90px (segment)

        self.slice = WIDTH // 5     # 256px
        self.segment = HEIGHT // 8  # 90px
        self.air = self.space = 10    # px
        self.shift = 20               # px

        self.buttons_hover_states = {"play": False, "options": False, "about": False, "exit": False, "gitlab": False}
        self.buttons_sprites = {
            "play": load(str(PurePath(PATH_IMAGES).joinpath("btn_play3.png"))).convert_alpha(),
            "options": load(str(PurePath(PATH_IMAGES).joinpath("btn_opt.png"))).convert_alpha(),
            "about": load(str(PurePath(PATH_IMAGES).joinpath("btn_about.png"))).convert_alpha(),
            "exit": load(str(PurePath(PATH_IMAGES).joinpath("btn_exit.png"))).convert_alpha(),
            "gitlab": load(str(PurePath(PATH_IMAGES).joinpath("btn_gitlab.png"))).convert_alpha(),
            "gitlab_h": load(str(PurePath(PATH_IMAGES).joinpath("btn_h_gitlab.png"))).convert_alpha()}

        # LOGO: 768x360px
        # horizontal - logo takes 3 parts out of 5 - W/5 * 3 = 768px
        # vertical - logo takes half of H - H/2 = 360px
        self.logo_rect = pygame.Rect(self.slice, 0, self.slice * 3, HEIGHT / 2)
        self.logo_image = load(str(PurePath(PATH_IMAGES).joinpath("logo_placeholder.png"))).convert_alpha()

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

        self.gitlab_button_rect = pygame.Rect(WIDTH - 100 - 20, HEIGHT - 100 - 20, 200, 200)
        self.buttons_dict = {"options": 5, "about": 6, "exit": 7}

    def draw(self, x: int, y: int)-> None:

        self.screen.fill(Color.dark_blue)
        self.screen.blit(self.logo_image, self.logo_rect)

        self._draw_play_button(x, y)
        self._draw_gitlab_button(x, y)

        for key in self.buttons_dict.keys():
            self._draw_other_buttons(x, y, key)
        pygame.display.update()

    def _draw_play_button(self, x: int, y: int)-> None:

        self.play_button_rect.top = self.segment * 4
        self.play_button_rect.left = self.space
        hovered = self._hovered(x, y, self.play_button_rect)

        if hovered:
            self.buttons_hover_states["play"] = True
            self.play_button_rect.left = self.shift
            self.screen.blit(self.buttons_sprites["play"], self.play_button_rect)
        else:
            self.buttons_hover_states["play"] = False
            self.play_button_rect.left = self.space
            self.screen.blit(self.buttons_sprites["play"], self.play_button_rect)

    def _draw_other_buttons(self, x: int, y: int, button: str)-> None:

        self.other_button_rect.top = self.segment * self.buttons_dict[button]
        hovered = self._hovered(x, y, self.other_button_rect)

        if hovered:
            self.buttons_hover_states[button] = True
            self.other_button_rect.left = self.shift
            self.screen.blit(self.buttons_sprites[button], self.other_button_rect)
        else:
            self.buttons_hover_states[button] = False
            self.other_button_rect.left = self.space
            self.screen.blit(self.buttons_sprites[button], self.other_button_rect)

    def _draw_gitlab_button(self, x: int, y: int)-> None:

        hovered = self._hovered(x, y, self.gitlab_button_rect)

        if hovered:
            self.buttons_hover_states["gitlab"] = True
            self.screen.blit(self.buttons_sprites["gitlab_h"], self.gitlab_button_rect)
        else:
            self.buttons_hover_states["gitlab"] = False
            self.screen.blit(self.buttons_sprites["gitlab"], self.gitlab_button_rect)

    def _hovered(self, x: int, y: int, button: object)-> bool:
        return button.collidepoint(x, y)

    def open_gitlab(self)->None:
        wb.open(GIT_LAB_LINK)