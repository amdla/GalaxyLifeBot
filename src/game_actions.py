from utils import ATTACK_BUTTON, FIND_TARGET_BUTTON, FIGHT_NOW_BUTTON, SPEED_UP_X2_BUTTON, END_BATTLE_BUTTON, \
    GO_HOME_BUTTON, TRAINING_CAMP_1_BUTTON, TRAINING_CAMP_2_BUTTON, ADD_LOOTERS_TO_TRAINING_LIST_BUTTON, \
    CHOOSE_LOOTER_UNIT_WHEN_ATTACKING_BUTTON, CLOSE_TRAINING_VIEW_BUTTON
from utils import click_and_wait


def search_for_enemy():
    """
    Performs the sequence of clicks to search for an enemy base.
    """
    try:
        click_and_wait(ATTACK_BUTTON, 1.5)
        click_and_wait(FIND_TARGET_BUTTON, 1.5)
        click_and_wait(FIGHT_NOW_BUTTON, 1.5)
        click_and_wait(FIGHT_NOW_BUTTON, 8)
    except Exception as e:
        raise e


def attack():
    """
    Performs an attack sequence including troop deployment and battle management.
    """

    try:
        deploy_troops()
        click_and_wait(SPEED_UP_X2_BUTTON, 0)
        click_and_wait(SPEED_UP_X2_BUTTON, 50)  # Wait for the battle to end (x4 speed)
        click_and_wait(END_BATTLE_BUTTON, 5)
        click_and_wait(GO_HOME_BUTTON, 10)

    except Exception as e:
        raise e


def deploy_troops():
    """
    Deploys troops in a specific pattern around the enemy base.
    """

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
        raise e


def add_troops_to_training():
    """
    Adds troops to the training queue in the training camps.
    """
    try:
        click_and_wait(TRAINING_CAMP_1_BUTTON, 0.1)
        click_and_wait(TRAINING_CAMP_1_BUTTON, 1.5)
        for _ in range(15):
            click_and_wait(ADD_LOOTERS_TO_TRAINING_LIST_BUTTON, 0.1)
        click_and_wait(TRAINING_CAMP_2_BUTTON, 0.1)
        click_and_wait(TRAINING_CAMP_2_BUTTON, 1.5)
        for _ in range(15):
            click_and_wait(ADD_LOOTERS_TO_TRAINING_LIST_BUTTON, 0.1)
        click_and_wait(CLOSE_TRAINING_VIEW_BUTTON, 1)
    except Exception as e:
        raise e
