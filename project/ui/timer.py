from pathlib import PurePath

import pygame as pg

from project.constants import Color, PATH_FONTS


class Timer:
    """
    Represent the text timer in the game.

<<<<<<< HEAD
    def __init__(self, game, _type, time: int, x: int, y: int, font: str, font_size: int, text: bool= False):
=======
    The timer counts down from given seconds.
    """
    def __init__(self, game, time: int, x: int, y: int, font: str, font_size: int):
        """
        Constructor for the timer.
        """
>>>>>>> c946aab6835f1aba7338c56e515252f73d4c1551
        self.game = game
        self.screen = self.game.screen
        self.game.nonsprite.add(self)

        self.x = x
        self.y = y

        self.display_text = text
        self.type = _type
        self.font = pg.font.Font(str(PurePath(PATH_FONTS).joinpath(font)), font_size)
        self.time = time
        self.start = pg.time.get_ticks()
        self.start_text = pg.time.get_ticks()
        self.completed = False
        self.show_text = False

    def draw(self)->None:
        """
        Bliting the timer on the screen.
        """
<<<<<<< HEAD

        self.effect_dict =\
            {
                'red': ' You got extra hp',
                'pink': 'Your hp is now full',
                'purple': 'Double shot!',
                'blue': 'You shield is now full',
                'yellow': 'You are now immune!',
                'white': 'You shoot faster!',
                'green': 'More armor!',
                'w_green': 'More damage!'
            }
=======
        if not self.completed:
            self.current = (pg.time.get_ticks() - self.start) // 1000
            if self.current <= self.time:
                self.text = self.font.render(self.min_sec(self.time - self.current), True, Color.white)
>>>>>>> c946aab6835f1aba7338c56e515252f73d4c1551

        if not self.display_text:
            if not self.completed:

                self.current = (pg.time.get_ticks() - self.start) // 1000

                if self.current <= self.time:
                    self.text = self.font.render(self.min_sec(self.time - self.current), True, Color.white)

                    self.screen.blit(self.text, (self.x, self.y))

        if self.display_text:
            if not self.show_text:
                self.current = (pg.time.get_ticks() - self.start_text) // 1000
                if self.current <= 2:
                    self.text_str = self.font.render(self.effect_dict[self.type], True, Color.white)

                    self.screen.blit(self.text_str, (100, 100))

    @staticmethod
    def min_sec(sec: int)->str:
        """
        Formats seconds to mitutes and second (m:ss).
        """
        return f'{int((sec - sec % 60) / 60)}:{sec % 60:02}'
