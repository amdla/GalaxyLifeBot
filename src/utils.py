import logging
import os
import shutil
import time

import pyautogui
from pygetwindow import getWindowsWithTitle

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
CLOSE_NEWS_POPUP_BUTTON = (1583, 204)
CLOSE_DAILY_GIFT_POPUP_BUTTON = (1590, 530)
DEFENSIVE_BUILDINGS_THRESHOLD = 3
GOLD_VALUE_THRESHOLD = 2137
MINERAL_VALUE_THRESHOLD = 2137

SCAN_WINDOW_DATA = [985, 100, 65, 50]
ATTACK_WINDOW_DATA = [1000, 855, 280, 45]


class IterationData:
    def __init__(self, uptime, iteration):
        self.uptime = uptime
        self.iteration = iteration
        self.detected_defensive_buildings = None
        self.opponent_gold_value = None
        self.opponent_mineral_value = None
        self.loot_gold_value = None
        self.loot_mineral_value = None
        self.is_base_on_edge = None
        self.is_worth_resources = None
        self.is_worth_defensive_buildings = None
        self.is_worth_total = None

    def set_opponent_values(self, opponent_gold_value, opponent_mineral_value):
        self.opponent_gold_value = int(opponent_gold_value)
        self.opponent_mineral_value = int(opponent_mineral_value)
        self.is_worth_resources = (int(opponent_gold_value) > GOLD_VALUE_THRESHOLD
                                   and int(opponent_mineral_value) > MINERAL_VALUE_THRESHOLD)

    def set_looted_values(self, loot_gold_value, loot_mineral_value):
        self.loot_gold_value = int(loot_gold_value)
        self.loot_mineral_value = int(loot_mineral_value)

    def set_defence_detections(self, amount_of_defensive_buildings, is_base_on_edge, worth_based_on_defence_result):
        self.detected_defensive_buildings = amount_of_defensive_buildings
        self.is_base_on_edge = is_base_on_edge
        self.is_worth_defensive_buildings = worth_based_on_defence_result
        self.is_worth_total = self.is_worth_resources and self.is_worth_defensive_buildings

    def print_all_data(self, logger):
        logger.info("--------------------------------------TEST FROM DATA CLASS--------------------------------------")
        logger.info("--------------------------------------TEST FROM DATA CLASS--------------------------------------")
        logger.info("--------------------------------------TEST FROM DATA CLASS--------------------------------------")
        logger.info(f"Iteration: {self.iteration}")
        logger.info(f"Uptime: {self.uptime}")
        logger.info(f"Detected defensive buildings: {self.detected_defensive_buildings}")
        logger.info(f"Opponent gold value: {self.opponent_gold_value}")
        logger.info(f"Opponent mineral value: {self.opponent_mineral_value}")
        logger.info(f"Looted gold value: {self.loot_gold_value}")
        logger.info(f"Looted mineral value: {self.loot_mineral_value}")
        logger.info(f"Is worth resources: {self.is_worth_resources}")
        logger.info(f"Is base on edge: {self.is_base_on_edge}")
        logger.info(f"Is worth defensive buildings: {self.is_worth_defensive_buildings}")
        logger.info(f"Is worth total: {self.is_worth_total}")
        logger.info("------------------------------------END TEST FROM DATA CLASS------------------------------------")
        logger.info("------------------------------------END TEST FROM DATA CLASS------------------------------------")
        logger.info("------------------------------------END TEST FROM DATA CLASS------------------------------------")


def clear_screenshots_directory():
    """
    Clears the screenshots directory by removing all files and recreating the directory.
    """

    directory = '../logs/screenshots'

    if os.path.exists(directory):
        shutil.rmtree(directory)
        os.makedirs(directory)
        with open(os.path.join(directory, '.gitkeep'), 'w'):
            pass

        logging.info(f"Directory '{directory}' has been cleared.")
    else:
        logging.info(f"Directory '{directory}' does not exist.")


def click_and_wait(button, time_to_wait):
    """
    Clicks a specified button and waits for a given amount of time.

    Params:
        button (tuple): The (x, y) coordinates of the button to click.
        time_to_wait (float): The number of seconds to wait after clicking.
    """

    pyautogui.click(button)
    time.sleep(time_to_wait)


def get_initial_base():
    """
    Navigates to the initial base.
    """

    try:
        click_and_wait(OPEN_PLANETS_LIST_BUTTON, 2)
        click_and_wait(COLONY_11_BUTTON, 7)
    except Exception as e:
        raise e


def handle_error():
    """
    Handles errors by refreshing the game window and resetting to the initial base.
    """

    get_screenshot("Galaxy Life")  # take focus on window
    logging.warning(
        "---------------------------------Handling error with F5 refresh---------------------------------")
    pyautogui.keyDown('F5')
    time.sleep(0.2)
    pyautogui.keyUp('F5')
    time.sleep(15)
    click_and_wait(CLOSE_NEWS_POPUP_BUTTON, 3)
    click_and_wait(CLOSE_DAILY_GIFT_POPUP_BUTTON, 2)

    get_initial_base()


def get_screenshot(window_title):
    """
    Captures a screenshot of a specified window.

    Params:
        window_title (str): The title of the window to capture

    Returns:
        Image: The captured screenshot
    """
    try:
        window = getWindowsWithTitle(window_title)[0]
        window.activate()
        time.sleep(0.25)
        window.maximize()
        time.sleep(0.25)
        window.moveTo(0, 0)
        time.sleep(0.25)
    except IndexError:
        logging.error("Window not found!")
        exit()
    return pyautogui.screenshot()


# TODO: list below
"""
# TODO: calculate efficiency?
as for efficiencies, i want them to be stored in new columns within our log table
mineral_efficiency = loot_mineral_value / mineral_value
gold_efficiency = loot_gold_value / gold_value
total_efficiency = (loot_mineral_value+loot_gold_value)/(mineral_value+gold_value)
at some point (maybe when starting the logger, we should save values assigned to threshholds for:
defensive_buildings, gold and mineral value (like the one that we use to decide if attack is worth it)
i want it to be printed over and over again for each entry in a separate column
-------------------
i want to add some kind of total logging that will be used to calculate stats for entire project
i want to keep logging stuff for each run separately, but i also want them to be logged to a one bigger logging
file (we will append new entries there)
like yk log1.xlsx log2.xlsx log3.xlsx for each run and all_logs.xlsx for file containing all the runs together
remember about new columns (especially the efficiency ones) and the fact that we have naming convention already
-------------------
i want all the logging to console be logged to some file, let's say logs.txt; new logs are gonna be appended to the file
####gotta fix it -> logs are cleared every time
"""
