from project.sprites.character import Character


class NonPlayerCharacter(Character):
    """ Base class for all NPC's """
    def init(*args):
        super().__init__(*args)
        self.add(self.game.enemy_sprites())
