import logging
from datetime import datetime

from game_actions import search_for_enemy, attack, add_troops_to_training
from image_processing import process_screenshot, is_worth_attacking
from utils import clear_screenshots_directory, get_screenshot, click_and_wait, handle_error, ExcelLogger, \
    SEARCH_AGAIN_BUTTON

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

global init_time
global workbook, sheet


def main_loop():
    """
    Loop that manages the overall flow of searching for enemies and attacking.
    """
    iterations = 0
    while True:
        try:
            search_for_enemy()
            while True:
                iterations += 1
                if iterations % 50 == 0:
                    raise Exception("Restarting the game after 50 iterations to avoid getting stuck.")
                gold_value, mineral_value, screen_path, uptime = process_screenshot(init_time)

                if is_worth_attacking(gold_value, mineral_value, screen_path):
                    excel_logger.log_to_excel(gold_value, mineral_value, True, uptime)
                    attack()
                    add_troops_to_training()
                    break
                else:
                    excel_logger.log_to_excel(gold_value, mineral_value, False, uptime)
                    click_and_wait(SEARCH_AGAIN_BUTTON, 8)

        except Exception as e:
            logging.error(f"Error: {e}")
            iterations = 0
            handle_error()


if __name__ == '__main__':
    init_time = datetime.now()
    excel_logger = ExcelLogger(init_time)
    workbook, sheet = None, None

    clear_screenshots_directory()
    get_screenshot("Galaxy Life")  # take focus on window
    main_loop()

# TODO: log error reading resources
