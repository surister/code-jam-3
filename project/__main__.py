from project.game import Game
from pygame import quit

if __name__ == '__main__':
    a = Game()
    a.show_start_screen()
    while a.running:
        a.new()
quit()
