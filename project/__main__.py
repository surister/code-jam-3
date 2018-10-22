from pygame import quit
from sprites import game


if __name__ == '__main__':
        a = game.Game()
        while a.running:
            a.new()
quit()
