import datetime
import os
import shutil
import time
from datetime import datetime

import pyautogui

import resource_extraction as re
from utils import handle_error


def remove_all_files_from_screenshots_directory():
    directory_path = "../../screenshots"
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f'Removed file: {file_path}')
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f'Removed directory: {file_path}')
    else:
        print(f'The directory {directory_path} does not exist')


def get_gold_and_mineral_values_and_filename():
    try:
        window_title = "Galaxy Life"
        screenshot = re.get_screenshot(window_title)

        # Generate a timestamp and save screen to file (for ML)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screen_path = f"../../screenshots/screen{timestamp}.png"
        screenshot.save(screen_path)

        if screenshot:
            gold_value, mineral_value = re.get_gold_and_minerals(screenshot)
            print(f"\n\n--------------------------------------------------------------------\n\n")
            print(f"Gold Value: {gold_value}")
            print(f"Mineral Value: {mineral_value}")
            return gold_value, mineral_value, screen_path
        return 0, 0
    except Exception as e:
        print(f"Error: {e}")
        handle_error()


def get_initial_base():
    try:
        time.sleep(2)
        pyautogui.click(940, 1320)
        time.sleep(2)
        pyautogui.click(1190, 1240)
        time.sleep(8)
    except Exception as e:
        print(f"Error: {e}")
        handle_error()


if __name__ == '__main__':
    try:
        remove_all_files_from_screenshots_directory()
        re.get_screenshot("Galaxy Life")
        from battle_actions import search_for_enemies

        search_for_enemies()
    except Exception as e:
        print(f"Error: {e}")
        handle_error()
