from project.sprites.non_player_character import NonPlayerCharacter


class Fighter(NonPlayerCharacter):
    """ Fighters circle around the player and rapidly shoot weak projectiles at him """
    def __init__(self, radius, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.radius = radius

    def update(self):
        player_pos = self.game.player_character.pos
        if player_pos.x > self.pos.x:
            self.acc.x += abs(player_pos.x - self.pos.x)/100
        else:
            self.acc.x -= abs(player_pos.x - self.pos.x)/100

        if player_pos.y > self.pos.y:
            self.acc.y += abs(player_pos.y - self.pos.y)/100
        else:
            self.acc.y -= abs(player_pos.y - self.pos.y)/100
        super().update()

        # print(f"pp:{player_pos}, fp: {self.pos}")
        # TODO add firing projectiles
