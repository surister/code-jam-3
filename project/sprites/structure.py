from project.sprites.non_player_character import NonPlayerCharacter

from pygame import Vector2
from pygame.sprite import Sprite


class Structure(NonPlayerCharacter):
    """ Structures slow move from off screen to their fixed position and then start firing at the player. """

    def __init__(
        self,
        game,
        health_points: int,
        defense: int,
        destination: Vector2,
        vel: Vector2,
        pos: Vector2
    ):
        super().__init__(game, health_points, defense, vel=vel, pos=pos)
        self.destination = destination
        self.arrived = False

    def update(self):
        """ Move to towards destination if not already there, otherwise shoot at the player """
        if not self.arrived:
            self.pos.x = self.pos.x - self.vel.x
            self.pos.y = self.pos.y - self.vel.y

            if self.pos == self.destination:
                self.arrived = True
        else:
            # TODO implement once projectiles are added to the game
            pass
        self.rect.midbottom = self.pos
        # Sprite.update(self)
