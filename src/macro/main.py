import logging

from resource_extraction import get_screenshot
from battle_actions import search_for_enemies

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    screenshot = get_screenshot("Galaxy Life")  # used just to take focus in window

    if screenshot:
        search_for_enemies()

    exit()
