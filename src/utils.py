import logging
import os
import shutil
import time

import pyautogui
from openpyxl import Workbook, load_workbook

from src.image_processing import get_screenshot


def clear_screenshots_directory():
    """
    Clears the screenshots directory by removing all files and recreating the directory.
    """

    directory = '../logs/screenshots'

    if os.path.exists(directory):
        shutil.rmtree(directory)
        os.makedirs(directory)
        with open(os.path.join(directory, '.gitkeep'), 'w') as f:
            pass

        logging.info(f"Directory '{directory}' has been cleared.")
    else:
        logging.info(f"Directory '{directory}' does not exist.")


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
    logging.warning("---------------------------------Handling error with F5 refresh---------------------------------")
    pyautogui.keyDown('F5')
    time.sleep(0.2)
    pyautogui.keyUp('F5')
    time.sleep(12)
    click_and_wait(CLOSE_NEWS_POPUP_BUTTON, 3)
    click_and_wait(CLOSE_DAILY_GIFT_POPUP_BUTTON, 2)

    get_initial_base()


class ExcelLogger:
    def __init__(self, init_time):
        self.init_time = init_time
        self.workbook = None
        self.sheet = None
        self.filename = None
        self.init_excel_logging()

    def init_excel_logging(self):
        """
        Initializes the Excel workbook for logging.
        """
        init_time_formatted = self.init_time.strftime("%Y%m%d_%H%M%S")
        self.filename = f"../logs/excel/{init_time_formatted}-log.xlsx"

        if os.path.exists(self.filename):
            self.workbook = load_workbook(self.filename)
            self.sheet = self.workbook.active
        else:
            self.workbook = Workbook()
            self.sheet = self.workbook.active
            headers = ["Gold Value", "Mineral Value", "Is Worth Attacking", "Uptime", "Looted Gold", "Looted Minerals",
                       "Gold efficiency", "Mineral efficiency"]
            for col, header in enumerate(headers, start=1):
                self.sheet.cell(row=1, column=col, value=header)

        self.workbook.save(self.filename)

    def log_to_excel(self, gold_value, mineral_value, is_worth, uptime, loot_gold_value, loot_mineral_value):
        """
        Logs data to the Excel spreadsheet.

        Params:
            gold_value (str): The gold value
            mineral_value (str): The mineral value
            is_worth (bool): True if the base is worth attacking, False otherwise
            uptime (timedelta): The bot's uptime
        """
        new_row = [gold_value, mineral_value, is_worth, uptime, loot_gold_value, loot_mineral_value]
        self.sheet.append(new_row)
        self.workbook.save(self.filename)
# TODO: calculate efficiency?
