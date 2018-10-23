from pygame import quit

from project.game import Game

if __name__ == '__main__':
    a = Game()
    while a.running:
        a.new()
quit()
