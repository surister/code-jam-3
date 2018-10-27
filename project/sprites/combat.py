from random import randint
from typing import List, Tuple

import pygame as pg

from project.sprites.game_elements import Item, Projectile


class Combat:
    def __init__(
        self,
        health: int,
        defence: int=0,
        armor: int=0,
        shield: int=0,
        points: int=0,
        fire_rate: int=250,
        drops: List[Tuple[Item, int]]=None
    ):
        """Class to handle combat for sprites that need it"""
        self.health = health
        self.defence = defence
        self.points = points
        self.shield = shield
        self.fire_rate = fire_rate
        self.armor = armor
        self.type: int = None
        # Type will tell us what kind of projectiles we'd shoot
        # 0 -> Foes
        # 1 -> Main character
        # 2 -> TBD
        if drops is None:
            self.drops = []
        else:
            self.drops = drops

        self.last_update = 0
        self.fire_rate = fire_rate

    def damage(self, projectile: Projectile) -> None:
        """dmg = projectile.damage
        s = self.shield
        self.shield -= dmg
        if self.shield < 0:
            dmg -= s"""
        if self.shield != 0:
            self.shield -= max(projectile.damage - max(self.armor - projectile.penetration, 0), 0)
        else:
            self.health -= max(projectile.damage - max(self.armor - projectile.penetration, 0), 0)
        if self.health <= 0:
            self._destroy()

    def _destroy(self) -> None:
        """Overwrite this in the sprite class if non-default behaviour is needed"""
        self.game.score += self.points
        self._generate_drops()
        self.kill()

    def _generate_drops(self) -> None:
        for drop in self.drops:
            if drop[1] < randint(100):
                drop[0].spawn(self.pos)

    def _shot(self, angle: float=0, spawn_point: pg.Vector2=None) -> None:
        now = pg.time.get_ticks()
        if now - self.last_update > self.fire_rate:
            self.last_update = now
            self.projectiles.append(
                Projectile(self.game, self, angle=angle, spawn_point=spawn_point)
            )
