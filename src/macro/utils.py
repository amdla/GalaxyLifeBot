import time
import pyautogui
import logging

from battle_actions import scan_enemy

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define button coordinates as constants
ATTACK_BUTTON = (935, 1365)
FIND_TARGET_BUTTON = (950, 1270)
FIGHT_NOW_BUTTON = (1360, 865)
SEARCH_AGAIN_BUTTON = (1030, 1305)
TRAINING_CAMP_1_BUTTON = (1265, 505)
TRAINING_CAMP_2_BUTTON = (1390, 565)
CLOSE_TRAINING_VIEW_BUTTON = (1615, 1340)
SPEED_UP_X2_BUTTON = (1535, 160)
END_BATTLE_BUTTON = (1475, 200)
GO_HOME_BUTTON = (1250, 935)
OPEN_PLANETS_LIST_BUTTON = (940, 1320)
COLONY_11_BUTTON = (1190, 1240)
ADD_LOOTERS_TO_TRAINING_LIST_BUTTON = (1070, 1420)
CHOOSE_LOOTER_UNIT_WHEN_ATTACKING_BUTTON = (950, 1375)


def click_and_wait(button, time_to_wait):
    pyautogui.click(button)
    time.sleep(time_to_wait)


def handle_error():
    from resource_extraction import get_screenshot
    get_screenshot("Galaxy Life")  # No need to store it, we need only to get focus on GL window
    logging.warning("Handling error with F5 refresh")
    pyautogui.keyDown('F5')
    time.sleep(0.2)
    pyautogui.keyUp('F5')
    time.sleep(15)
    from main import search_for_enemies
    get_initial_base()
    search_for_enemies()


def get_initial_base():
    try:
        click_and_wait(OPEN_PLANETS_LIST_BUTTON, 2)
        click_and_wait(COLONY_11_BUTTON, 2)
        time.sleep(8)  # Wait for the base to load
    except Exception as e:
        logging.error(f"Error: {e}")
        handle_error()


def is_worth_attacking(gold, mineral, screen_path):
    from predict import is_worth_based_on_defences
    try:
        result = int(gold) + int(mineral) > 1500000 and is_worth_based_on_defences(screen_path)
        logging.info(f"Is worth attacking: {result}")
        if result:
            from battle_actions import attack
            attack()
        else:
            click_and_wait(SEARCH_AGAIN_BUTTON, 10)
            scan_enemy()
    except Exception as e:
        logging.error(f"Error: {e}")
        handle_error()
