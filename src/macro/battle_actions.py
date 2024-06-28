import time

import pyautogui

from main import get_gold_and_mineral_values_and_filename
from utils import handle_error, is_worth_attacking


def search_for_enemies():
    try:
        pyautogui.click(935, 1365)  # attack
        time.sleep(2.5)
        pyautogui.click(950, 1270)  # find_target
        time.sleep(2.5)
        pyautogui.click(1360, 865)  # fight_now
        time.sleep(2.5)
        pyautogui.click(1360, 865)  # fight_now
        time.sleep(2.5)
        wait_for_battle(10)
    except Exception as e:
        print(f"Error: {e}")
        handle_error()


def wait_for_battle(seconds):
    try:
        time.sleep(seconds)
        gold_value, mineral_value, filename = get_gold_and_mineral_values_and_filename()
        if is_worth_attacking(gold_value, mineral_value, filename):
            attack()
        else:
            pyautogui.click(1030, 1305)  # search_again
            wait_for_battle(10)
    except Exception as e:
        print(f"Error: {e}")
        handle_error()


def deploy_troops():
    try:
        pyautogui.click(950, 1375)
        time.sleep(0.5)
        coordinates = [
            (1460, 290), (1695, 435), (1870, 525), (1980, 590), (2090, 620),
            (2210, 685), (2340, 800), (2210, 870), (2060, 955), (1915, 1030),
            (1800, 1090), (1650, 1150), (1420, 1230), (1135, 1220), (855, 1160),
            (600, 1055), (390, 930), (245, 740), (380, 620), (630, 500),
            (840, 405), (1000, 310)
        ]
        for x, y in coordinates:
            pyautogui.click(x, y)
            time.sleep(0.1)
    except Exception as e:
        print(f"Error: {e}")
        handle_error()


def add_troops_to_training():
    try:
        times = 30
        time.sleep(2)
        pyautogui.click(1265, 505)  # training camp 1
        time.sleep(0.3)
        pyautogui.click(1265, 505)  # training camp 1
        time.sleep(2)
        for _ in range(times):
            pyautogui.click(1070, 1420)
            time.sleep(0.1)
        pyautogui.click(1390, 565)  # training camp 2
        time.sleep(0.3)
        pyautogui.click(1390, 565)  # training camp 2
        time.sleep(2)
        for _ in range(times):
            pyautogui.click(1070, 1420)
            time.sleep(0.1)
        pyautogui.click(1615, 1340)  # close view
        time.sleep(1)
        search_for_enemies()
    except Exception as e:
        print(f"Error: {e}")
        handle_error()


def attack():
    try:
        deploy_troops()
        pyautogui.click(1535, 160)  # speed up x2
        pyautogui.click(1535, 160)  # speed up x4
        time.sleep(60)
        pyautogui.click(1475, 200)  # end_battle
        time.sleep(1)
        pyautogui.click(1250, 935)  # go_home
        time.sleep(10)
        add_troops_to_training()
    except Exception as e:
        print(f"Error: {e}")
        handle_error()
