import logging

from pygame import quit

from project.game import Game

LOG_LEVEL = logging.INFO

# initialize the logger, set LOG_LEVEL to change what messages get logged to the console
last_judgment_logger = logging.getLogger('last_judgment_logger')
last_judgment_logger.setLevel(LOG_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(LOG_LEVEL)
last_judgment_logger.addHandler(stream_handler)

last_judgment_logger.info('Welcome to Last Judgment')

if __name__ == '__main__':
    a = Game()
    a.show_start_screen()
    a.play_intro()
    while a.running:
        a.new()
quit()
