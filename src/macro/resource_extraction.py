import time
import easyocr
import numpy as np
import pyautogui
import pygetwindow as gw
import torch
import logging
from utils import handle_error

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_region_of_interest(image, x, y, width, height):
    try:
        return image[y:y + height, x:x + width]
    except Exception as e:
        logging.error(f"Error: {e}")
        handle_error()


def split_region_of_interest_for_gold_and_mineral_fields(region_of_interest):
    try:
        mid_index = region_of_interest.shape[0] // 2
        return region_of_interest[:mid_index, :], region_of_interest[mid_index:, :]
    except Exception as e:
        logging.error(f"Error: {e}")
        handle_error()


def read_gold_and_mineral_values(region_of_interest, reader):
    try:
        result = reader.readtext(np.array(region_of_interest), detail=0)
        return ''.join(filter(str.isdigit, ''.join(result)))
    except Exception as e:
        logging.error(f"Error: {e}")
        handle_error()


def get_gold_and_minerals(screenshot):
    try:
        screenshot_np = np.array(screenshot.convert('L'))
        region_of_interest = extract_region_of_interest(screenshot_np, 985, 100, 65, 50)

        with torch.no_grad():
            reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())

        split_regions_of_interest = split_region_of_interest_for_gold_and_mineral_fields(region_of_interest)
        gold_value = read_gold_and_mineral_values(split_regions_of_interest[0], reader)
        mineral_value = read_gold_and_mineral_values(split_regions_of_interest[1], reader)

        return gold_value, mineral_value
    except Exception as e:
        logging.error(f"Error: {e}")
        handle_error()


def get_screenshot(window_title):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        window.activate()
        time.sleep(0.25)
        window.maximize()
        time.sleep(0.25)
        window.moveTo(0, 0)
        time.sleep(0.25)
    except IndexError:
        logging.warning("Window not found!")
        handle_error()
    return pyautogui.screenshot()
