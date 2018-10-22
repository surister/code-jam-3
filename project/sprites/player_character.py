from project.sprites.character import Character

class PlayerCharacter(Character):
    #TODO determine base stats for the character

    def update(self) -> None:
        self.key = pygame.key.get_pressed()
        
        # Can't detect UP and Down key??
        self.acc.y = self.acc.x = 0
        if self.key[pygame.KEYUP] or self.key[pygame.K_w]:
            self.acc.y = -1
        if self.key[pygame.KEYDOWN] or self.key[pygame.K_s]:
            self.acc.y = 1
        if self.key[pygame.K_LEFT] or self.key[pygame.K_a]:
            self.acc.x = -1
        if self.key[pygame.K_RIGHT] or self.key[pygame.K_d]:
            self.acc.x = 1
