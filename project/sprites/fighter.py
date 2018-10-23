from project.sprites.non_player_character import NonPlayerCharacter

from pygame import Vector2
from pygame.sprite import Sprite

class Fighter(NonPlayerCharacter):
    """ Fighters circle around the player and rapidly shoot weak projectiles at him """
    def __init__(self, radius, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.radius = radius

    def update(self):
        player_pos = self.game.player_character.pos
        if player_pos.x > self.pos.x:
            self.acc.x += 0.5
        else:
            self.acc.x -= 0.5
        
        if player_pos.y > self.pos.y:
            self.acc.y += 0.5
        else:
            self.acc.y -= 0.5      
        super().update()

        # print(f"pp:{player_pos}, fp: {self.pos}")
        
        # TODO add firing projectiles