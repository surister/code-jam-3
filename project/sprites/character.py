from pygame.sprite import Sprite
from pygame import Vector2
from project.sprites.dev_character import Physics
from constants import HEIGHT, WIDTH


class Character(Physics, Sprite):

    def __init__(
        self, 
        health_points -> int,
        defense -> int,
        position_x -> int,
        position_y -> int, 
        acceleration_x -> int=0, 
        acceleration_y -> int=0, 
        velocity_x -> int=0, 
        velocity_y -> 
        int=0, 
        weapons=[], 
        friction=0.1
        ):  
            
        super().__init__(friction)
        self.health_points = health_points
        self.defense = defense
        self.weapons = weapons
        self.pos = Vector2(position_x, position_y)
        self.acc = pygame.Vector2(acceleration_x, acceleration_y)
        self.vel = pygame.Vector2(velocity_x, velocity_y)

