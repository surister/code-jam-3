from collections import deque


class Levels:

    def __init__(self, game):
        self.game = game
        self.level = 0
        self.enemies = deque()
