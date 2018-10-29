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
        attack: int=2,
    ):
        """Class to handle combat for sprites that need it"""
        self.health = health
        self.max_health: int = health
        self.defence = defence
        self.points = points
        self.shield = shield
        self.max_shield = self.max_health/2
        self.fire_rate = fire_rate
        self.armor = armor
        self.attack = attack
        self.type: int = None
        self.projectile_scale: int = 1
        # Type will tell us what kind of projectiles we'd shoot
        # 0 -> Main character
        # 1 -> Normal foe
        # 2 -> Small foe

        self.last_update = 0
        self.fire_rate = fire_rate

    def damage(self, game, projectile: Projectile) -> None:
        """dmg = projectile.damage
        s = self.shield
        self.shield -= dmg
        if self.shield < 0:
            dmg -= s"""

        self.game = game

        if self.shield > 0:
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
        Item(self.game)

    def _shot(self, angle: float=0, spawn_point: pg.Vector2=None) -> None:
        now = pg.time.get_ticks()
        if now - self.last_update > self.fire_rate:
            self.last_update = now
            self.projectiles.append(
                Projectile(self.game, self, angle=angle, spawn_point=spawn_point, damage=self.attack)
            )
