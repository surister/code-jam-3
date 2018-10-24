import math

from project.sprites.non_player_character import NonPlayerCharacter


class Fighter(NonPlayerCharacter):
    """ Fighters circle around the player and rapidly shoot weak projectiles at him """
    def __init__(self, radius, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.radius = radius

    def update(self):
        player_pos = self.game.player_character.pos

        angle = math.atan2(player_pos.x - self.pos.x, self.pos.y - player_pos.y)
        if angle < 0:
            angle += math.tau

        self.acc.y -= math.cos(angle)
        self.acc.x += math.sin(angle)
        super().update()
