from project.sprites.non_player_character import NonPlayerCharacter


class Structure(NonPlayerCharacter):
    """ Structures slow move from off screen to their fixed position and then start firing at the player. """

    def __init__(
        self,
        game,
        health_points: int,
        defense: int,
        destination: int,
        vel,
        pos
    ):
        super().__init__(game, health_points, defense, vel=vel, pos=pos)
        self.destination = destination
        self.arrived = False

    def update(self):
        """ Move left untill destination passed if not already there, otherwise shoot at the player """
        if not self.arrived:
            self.pos.x = self.pos.x - self.vel.x

            if self.pos.x < self.destination:
                self.arrived = True
        else:
            # TODO implement once projectiles are added to the game
            pass
        self.rect.midbottom = self.pos
