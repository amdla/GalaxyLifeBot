import time
import pyautogui


def handle_error():
    pyautogui.keyDown('F5')
    time.sleep(0.2)
    pyautogui.keyUp('F5')
    time.sleep(15)
    from main import get_initial_base, search_for_enemies
    get_initial_base()
    search_for_enemies()


def is_worth_attacking(gold, mineral, screen_path):
    from predict import is_worth_based_on_defences
    try:
        result = int(gold) + int(mineral) > 1500000 and is_worth_based_on_defences(screen_path)
        print(f"Is worth attacking: {result}")
        return result
    except Exception as e:
        print(f"Error: {e}")
        handle_error()
