from pathlib import PurePath

from project.constants import PATH_IMAGES
from project.sprites.sheet import Sheet


class Intro:

    def __init__(self):

        self.slides_sheet = Sheet(str(PurePath(PATH_IMAGES).joinpath("slidesheet.png")))
        self.music = []
        self.sounds = []

    def display():
        pass
