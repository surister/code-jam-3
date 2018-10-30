from pathlib import PurePath
from random import randint

import pygame as pg
pg.mixer.init()

# Frame rate options
MIN_FPS = False
SHOW_FPS = True
FPS = 60

if MIN_FPS:
    FPS = 30

# Screen options
Full_Screen = False

WIDTH = 1280
HEIGHT = 720

WIDTH_RATIO = 1
HEIGHT_RATIO = 1

if Full_Screen:
    WIDTH = 1920
    HEIGHT = 1080
    WIDTH_RATIO = 1920 / WIDTH
    HEIGHT_RATIO = 1080 / HEIGHT


# Char consts
MAX_SPEED = 10
PLAYER_ACC = 1.5
FIRE_RATE = 250  # interval between shots: milliseconds

POWERUP_EFFECT = {
    'red': randint(15, 30),  # Hp
    'pink': 100,    # Full hp - don't change
    'purple': 15,   # double shot - seconds
    'blue': None,    # Full shield - don't change
    'yellow': 15,   # immune - seconds
    'white': 15,    # permanent extra fire rate
    'green': 5,     # +armor
    'w_green': 1    # + attack
}


class Color:
    white = (255, 255, 255)
    dark_blue = (41, 41, 66)
    dark_yellow = (109, 94, 10)
    red = (255, 0, 0)
    green = (106, 0, 100)
    pure_green = (0, 255, 0)
    pure_blue = (0, 0, 255)
    light_green = (20, 211, 136)
    black = (0, 0, 0)


PATH_PROJECT = PurePath(__file__).parent

PATH_SPRITES = PurePath(PATH_PROJECT).joinpath('sprites/')
PATH_ASSETS = PurePath(PATH_PROJECT).joinpath('assets/')
PATH_IMAGES = PurePath(PATH_PROJECT).joinpath('assets/images')
PATH_FONTS = PurePath(PATH_PROJECT).joinpath('assets/fonts')

PATH_MENUS = PurePath(PATH_PROJECT).joinpath('ui/')
PATH_GUI = PurePath(PATH_PROJECT).joinpath('assets/gui')
PATH_BUTTONS = PurePath(PATH_PROJECT).joinpath('assets/gui/buttons')
PATH_CURSORS = PurePath(PATH_PROJECT).joinpath('assets/gui/cursors')
PATH_BACKGROUNDS = PurePath(PATH_PROJECT).joinpath('assets/gui/backgrounds')

PATH_FX = PurePath(PATH_PROJECT).joinpath('assets/fx')
PATH_VOICES = PurePath(PATH_PROJECT).joinpath('assets/fx/slidevoices')


PROJECTILE_IMAGE_NAME = {0: 'blasters/b0.png',
                         1: 'blasters/b1.png',
                         2: 'blasters/b2.png',
                         3: 'blasters/b3.png',
                         4: 'blasters/b4.png',
                         5: 'blasters/b5.png',
                         6: 'blasters/b6.png'
                         }

CHARACTER_IMAGE_NAME = 'ufo3.png'
STRUCTURE_IMAGE_NAME = 'structure.png'
FIGHTER_IMAGE_NAME = 'fighter.png'
MINE_IMAGE_NAME = 'mine.png'
HEALTHBAR = 'healthbar.png'
SHIELDBAR = 'shield.png'
BUTTONSHEET = 'buttonsheet.png'
BACKGROUND = 'background.png'
BACKGROUND_2 = 'background2.png'
BACKGROUND_3 = 'background3.png'
VOLUME = 'volume.png'
VOLUME_NO = 'novolume.png'
BACK_BUTTON = 'back.png'
LABEL = 'label7.png'
LOGO = 'logo.png'
CURSOR = 'cur.png'
CURSOR_HOVER = 'hov.png'
PYTHON_LOGO = 'python_logo2.png'
PYTHON_LOGO_HOVER = 'python_logo_hover.png'
MISTY_HATS_LOGO = 'mistyhats.png'
MISTY_HATS_LOGO_HOVER = 'mistyhats_hover.png'
SWITCH = 'switch.png'

GIT_LAB_LINK = 'https://gitlab.com/JannesJ/code-jam-3'
PYTHON_DISCORD_LINK = 'https://pythondiscord.com/'
MISTY_LINK = 'https://pythondiscord.com/jams/team/6f243fac-4803-48bb-80f4-237d206e0fab'
POWERUPS = 'powerup_spritesheet.png'

DEFAULT_FONT_NAME = 'LiberationMono-Regular.ttf'

CHARACTER_SPACESHIP = 'own_spaceship.png'
INVISIBLE = (8, 8), (0, 0), ((0,) * 8), ((0,) * 8)  # invisible cursor

HOVER_SOUND = pg.mixer.Sound(str(PurePath(PATH_FX).joinpath('hover.wav')))
