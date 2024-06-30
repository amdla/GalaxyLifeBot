import logging
from datetime import datetime
from resource_extraction import get_gold_and_minerals, get_screenshot
from utils import (handle_error, is_worth_attacking, click_and_wait, ATTACK_BUTTON, FIND_TARGET_BUTTON,
                   FIGHT_NOW_BUTTON, TRAINING_CAMP_1_BUTTON, TRAINING_CAMP_2_BUTTON, CLOSE_TRAINING_VIEW_BUTTON,
                   SPEED_UP_X2_BUTTON, END_BATTLE_BUTTON, GO_HOME_BUTTON, ADD_LOOTERS_TO_TRAINING_LIST_BUTTON,
                   CHOOSE_LOOTER_UNIT_WHEN_ATTACKING_BUTTON)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def search_for_enemies():
    try:
        click_and_wait(ATTACK_BUTTON, 2.5)
        click_and_wait(FIND_TARGET_BUTTON, 2.5)
        click_and_wait(FIGHT_NOW_BUTTON, 2.5)
        click_and_wait(FIGHT_NOW_BUTTON, 10)
        scan_enemy()
    except Exception as e:
        logging.error(f"Error: {e}")
        handle_error()


def process_screenshot():
    try:
        window_title = "Galaxy Life"
        screenshot = get_screenshot(window_title)

        if screenshot:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screen_path = f"../../screenshots/screen{timestamp}.png"
            screenshot.save(screen_path)

            gold_value, mineral_value = get_gold_and_minerals(screenshot)
            logging.info("--------------------------------------------------------------------")
            logging.info(f"Gold Value: {gold_value}")
            logging.info(f"Mineral Value: {mineral_value}")
            return gold_value, mineral_value, screen_path

    except Exception as e:
        logging.error(f"Error: {e}")
        handle_error()


def scan_enemy():
    try:
        gold_value, mineral_value, filename = process_screenshot()
        is_worth_attacking(gold_value, mineral_value, filename)

    except Exception as e:
        logging.error(f"Error: {e}")
        handle_error()


def deploy_troops():
    try:
        click_and_wait(CHOOSE_LOOTER_UNIT_WHEN_ATTACKING_BUTTON, 0.5)
        coordinates = [
            (1460, 290), (1695, 435), (1870, 525), (1980, 590), (2090, 620),
            (2210, 685), (2340, 800), (2210, 870), (2060, 955), (1915, 1030),
            (1800, 1090), (1650, 1150), (1420, 1230), (1135, 1220), (855, 1160),
            (600, 1055), (490, 930), (445, 740), (480, 620), (630, 500),
            (840, 405), (1000, 310)
        ]
        for x, y in coordinates:
            click_and_wait((x, y), 0.1)
    except Exception as e:
        logging.error(f"Error: {e}")
        handle_error()


def add_troops_to_training():
    try:
        click_and_wait(TRAINING_CAMP_1_BUTTON, 2.5)
        for _ in range(30):
            click_and_wait(ADD_LOOTERS_TO_TRAINING_LIST_BUTTON, 0.1)
        click_and_wait(TRAINING_CAMP_2_BUTTON, 2.5)
        for _ in range(30):
            click_and_wait(ADD_LOOTERS_TO_TRAINING_LIST_BUTTON, 0.1)
        click_and_wait(CLOSE_TRAINING_VIEW_BUTTON, 1)
        search_for_enemies()
    except Exception as e:
        logging.error(f"Error: {e}")
        handle_error()


def attack():
    try:
        deploy_troops()
        click_and_wait(SPEED_UP_X2_BUTTON, 0)
        click_and_wait(SPEED_UP_X2_BUTTON, 60)  # Wait for the battle to end (x4 speed)
        click_and_wait(END_BATTLE_BUTTON, 1)
        click_and_wait(GO_HOME_BUTTON, 10)
        add_troops_to_training()
    except Exception as e:
        logging.error(f"Error: {e}")
        handle_error()
