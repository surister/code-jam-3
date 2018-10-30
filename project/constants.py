import json
from pathlib import PurePath

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

PATH_MENUS = PurePath(PATH_PROJECT).joinpath('ui/')
PATH_GUI = PurePath(PATH_PROJECT).joinpath('assets/gui')
PATH_BUTTONS = PurePath(PATH_PROJECT).joinpath('assets/gui/buttons')
PATH_CURSORS = PurePath(PATH_PROJECT).joinpath('assets/gui/cursors')
PATH_BACKGROUNDS = PurePath(PATH_PROJECT).joinpath('assets/gui/backgrounds')

PATH_FX = PurePath(PATH_PROJECT).joinpath('assets/fx')
PATH_VOICES = PurePath(PATH_PROJECT).joinpath('assets/fx/slidevoices')

with open(str(PurePath(PATH_PROJECT).joinpath("data.json"))) as f:
    DATA = json.load(f)


CHARACTER_IMAGE_NAME = "ufo3.png"
STRUCTURE_IMAGE_NAME = "structure.png"
PROJECTILE_IMAGE_NAME = {0: "blasters/b0.png",
                         1: "blasters/b1.png",
                         2: "blasters/b2.png",
                         3: "blasters/b3.png",
                         4: "blasters/b4.png",
                         5: "blasters/b5.png",
                         6: "blasters/b6.png"
                         }

FIGHTER_IMAGE_NAME = "fighter.png"
MINE_IMAGE_NAME = "mine.png"
HEALTHBAR = 'healthbar.png'
SHIELDBAR = 'shield.png'
BUTTONSHEET = "buttonsheet.png"
BACKGROUND = "background.png"
BACKGROUND_3 = "background3.png"
LOGO = "logo.png"
CURSOR = "cur.png"
CURSOR_HOVER = "hov.png"

GIT_LAB_LINK = "https://gitlab.com/JannesJ/code-jam-3"
PYTHON_DISCORD_LINK = "https://pythondiscord.com/"
MISTY_LINK = "https://pythondiscord.com/jams/team/6f243fac-4803-48bb-80f4-237d206e0fab"

INVISIBLE = (8, 8), (0, 0), ((0,) * 8), ((0,) * 8)  # invisible cursor

HOVER_SOUND = pg.mixer.Sound(str(PurePath(PATH_FX).joinpath("hover.wav")))

print(FPS)
print(WIDTH_RATIO, HEIGHT_RATIO, WIDTH, HEIGHT)
