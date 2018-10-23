from pygame import Surface, Vector2
from pygame.sprite import Sprite

from project.constants import Color
from project.sprites.dev_character import Physics


class Character(Physics, Sprite):
    """ Base class for Character, current implementation based on dev_character  """

    def __init__(
        self,
        game,
        health_points: int,
        defense: int,
        pos: Vector2 = None,
        acc: Vector2 = None,
        vel: Vector2 = None,
        weapons: list = None,
        friction: int = 0.1,
        image: Surface = None
    ):

        super().__init__(friction)
        self.game = game
        if image is None:
            self.image = Surface((50, 50))
        else:
            self.image = image
        self.rect = self.image.get_rect()  # going by the dev_char for now, should change later

        self.health_points = health_points
        self.defense = defense
        if weapons is None:
            self.weapons = []
        else:
            self.weapons = weapons

        if pos is None:
            self.pos = Vector2(0, 0)
        else:
            self.pos = pos

        if acc is None:
            self.acc = Vector2(0, 0)
        else:
            self.acc = acc

        if vel is None:
            self.vel = Vector2(0, 0)
        else:
            self.vel = vel

        self.friction = friction

        self.image.set_colorkey(Color.green)
        self.add(self.game.all_sprites)

    def update(self):
        # print(f"acc: {self.acc}, vel: {self.vel}, pos: {self.pos}, friction:{self.friction}")
        super().update()
