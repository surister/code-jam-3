from project.sprites.character import Character


class NonPlayerCharacter(Character):
    """ Base class for all NPC's """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add(self.game.enemy_sprites)
