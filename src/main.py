import logging
from datetime import datetime

from const_values import SEARCH_AGAIN_BUTTON
from game_actions import search_for_enemy, attack, add_troops_to_training
from image_processing import process_screenshot, is_worth_attacking, get_gold_and_minerals
from utils import clear_screenshots_directory, click_and_wait, handle_error, IterationData, get_screenshot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

global init_time


def main_loop():
    """
    Loop that manages the overall flow of searching for enemies and attacking.
    """
    iteration = 0
    while True:
        iteration_data = None
        try:
            search_for_enemy()
            while True:
                logging.info("---------------------------------------new enemy---------------------------------------")
                iteration_data = None
                iteration += 1
                uptime = (datetime.now() - init_time).total_seconds()
                logging.info(f"Uptime: {uptime}")

                iteration_data = IterationData(uptime, iteration)
                if iteration % 50 == 0:
                    raise Exception("Restarting the game after 50 iterations to avoid getting stuck.")

                gold_value, mineral_value, screen_path = process_screenshot()
                iteration_data.set_opponent_values(gold_value, mineral_value)

                if is_worth_attacking(gold_value, mineral_value, screen_path, iteration_data):
                    end_battle_screenshot = attack()
                    loot_gold_value, loot_mineral_value = get_gold_and_minerals(end_battle_screenshot, "battle")

                    iteration_data.set_looted_values(loot_gold_value, loot_mineral_value)
                    add_troops_to_training()
                    iteration_data.print_all_data(logging)
                    break
                else:
                    iteration_data.print_all_data(logging)
                    click_and_wait(SEARCH_AGAIN_BUTTON, 8)

        except Exception as e:
            logging.error(f"Error: {e}")
            if iteration_data:
                iteration_data.print_all_data(logging)
            handle_error()


if __name__ == '__main__':
    init_time = datetime.now()

    clear_screenshots_directory()
    get_screenshot("Galaxy Life")  # take focus on window
    main_loop()
