import logging
import time
from datetime import datetime

import cv2
import easyocr
import numpy as np
import pyautogui
import torch
from pygetwindow import getWindowsWithTitle
from ultralytics import YOLO


def save_detection_results(screen_path, results):
    """
    Saves detection results to a file and draws bounding boxes on the image.

    Params:
        screen_path (str): Path to the screenshot image
        results: Detection results from the YOLO model

    Returns:
        A tuple (result_path, image) containing:
        - result_path (str): Path to the detection results file
        - image: Image with bounding boxes drawn
    """
    try:
        result_path = f"{screen_path}.txt"
        image = cv2.imread(screen_path)

        with open(result_path, 'w') as f:
            f.write(f"Total detected boxes: {len(results.boxes.data)}\n")
            f.write("Detected boxes and their scores:\n")
            for result in results.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = result
                f.write(f"{class_id},{score},{x1},{y1},{x2},{y2}\n")
                if score > 0.2:
                    cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                    cv2.putText(image, results.names[int(class_id)].upper(), (int(x1), int(y1) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 2, cv2.LINE_AA)

        return result_path, image
    except Exception as e:
        raise e


def parse_detection_file(result_path):
    """
    Parses a detection file to extract base coordinates and detections.

    Params:
        result_path (str): The path to the detection results file.
    # TODO: handle None for base_coords!!!!
    Returns:
        A tuple (base_coords, detections) containing:
        - base_coords (tuple of 4 floats | None): Coordinates of the base, or None if not found.
        - detections (list): A list of tuples (each consisting of 4 floats) detection coordinates.
    """

    try:
        with open(result_path, 'r') as file:
            lines = file.readlines()

        base_coords = None
        detections = []

        for line in lines:
            parts = line.strip().split(',')
            if len(parts) == 6:
                class_id, score, x1, y1, x2, y2 = map(float, parts)
                if int(class_id) == 7:
                    base_coords = (x1, y1, x2, y2)
                detections.append((x1, y1, x2, y2))

        return base_coords, detections
    except Exception as e:
        raise e


def calculate_detections_deltas(detections, base_coords):
    """
    Calculates deltas of detections (max and min for both x and y values), and determines if the base is on the edge.

    Params:
        detections (list): A list of tuples (each consisting of 4 floats) detection coordinates.
        base_coords (tuple of 4 floats | None): Coordinates of the base, or None if not found.

    Returns:
        A tuple (deltas, is_base_on_edge) containing:
        - deltas (tuple of 4 floats): The delta values for the rectangle corners
        - is_base_on_edge (bool): True if the base is on the edge
    """
    # TODO: decide whether delta should be for all detections or just these with score > 0.33 (its for all now probably)
    # updated 0.33 to 0.2
    try:
        if not detections or base_coords is None:
            return

        x1_values = [coords[0] for coords in detections]
        x2_values = [coords[2] for coords in detections]
        y1_values = [coords[1] for coords in detections]
        y2_values = [coords[3] for coords in detections]

        deltas = [
            min(x1_values),
            max(x2_values),
            min(y1_values),
            max(y2_values)
        ]

        is_base_on_edge = (base_coords and
                           (base_coords[0] == deltas[0] or base_coords[2] == deltas[1] or
                            base_coords[1] == deltas[2] or base_coords[3] == deltas[3]))

        return deltas, is_base_on_edge
    except Exception as e:
        raise e


def read_resource_values(region_of_interest, reader):
    """
    Reads resource values from a region of interest using OCR.

    Params:
        region_of_interest (numpy.ndarray): The region to read from
        reader: An EasyOCR reader object

    Returns:
        str: The extracted numeric value as a string
    """

    try:
        result = reader.readtext(np.array(region_of_interest), detail=0)
        return ''.join(filter(str.isdigit, ''.join(result)))
    except Exception as e:
        raise e


def get_gold_and_minerals(screenshot):
    """
    Extracts gold and mineral values from a screenshot.

    Params:
        screenshot: The screenshot image

    Returns:
        tuple(gold_value, mineral_value) containing:
        - gold_value (str): The extracted gold value
        - mineral_value (str): The extracted mineral value
    """
    try:
        screenshot_np = np.array(screenshot.convert('L'))
        region_of_interest = extract_region_of_interest(screenshot_np, 985, 100, 65, 50)

        with torch.no_grad():
            reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())

        split_regions_of_interest = split_region_of_interest_for_gold_and_mineral_fields(region_of_interest)
        gold_value = read_resource_values(split_regions_of_interest[0], reader)
        mineral_value = read_resource_values(split_regions_of_interest[1], reader)

        return gold_value, mineral_value
    except Exception as e:
        raise e


def extract_region_of_interest(image, x, y, width, height):
    """
    Extracts a region of interest from an image.

    Params:
        image: The source image
        x (int): X-coordinate of the top-left corner
        y (int): Y-coordinate of the top-left corner
        width (int): Width of the region
        height (int): Height of the region

    Returns:
        numpy.ndarray: The extracted region of interest
    """
    try:
        return image[y:y + height, x:x + width]
    except Exception as e:
        raise e


def split_region_of_interest_for_gold_and_mineral_fields(region_of_interest):
    """
    Splits a region of interest into two parts for gold and mineral fields.

    Params:
        region_of_interest (numpy.ndarray): The region of interest to split

    Returns:
        tuple: Two numpy arrays (numpy.ndarray) representing the split regions
    """
    try:
        mid_index = region_of_interest.shape[0] // 2
        return region_of_interest[:mid_index, :], region_of_interest[mid_index:, :]
    except Exception as e:
        raise e


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


def process_screenshot(init_time):
    """
    Processes a screenshot to extract gold and mineral values. Saves bot's uptime to a file.

    Returns:
        gold_value (str): gold value
        mineral_value (str): mineral value
        screen_path (str): path to the saved screenshot
        uptime (timedelta): bot's uptime
    """
    try:
        window_title = "Galaxy Life"
        screenshot = get_screenshot(window_title)

        if screenshot:
            now = datetime.now()
            uptime = now - init_time

            timestamp = now.strftime("%Y%m%d_%H%M%S")
            screen_path = f"../logs/screenshots/{timestamp}.png"
            screenshot.save(screen_path)

            gold_value, mineral_value = get_gold_and_minerals(screenshot)

            logging.info(f"Gold Value: {gold_value}")
            logging.info(f"Mineral Value: {mineral_value}")
            logging.info(f"Uptime: {uptime}")

            return gold_value, mineral_value, screen_path, uptime

    except Exception as e:
        raise e


def is_worth_attacking(gold_value, mineral_value, screen_path):
    """
    Determines if a base is worth attacking based on resources and defences.

    Params:
        gold_value (str): gold value
        mineral_value (str): mineral value
        screen_path (str): Path to the screenshot image

    Returns:
        bool: True if the base is worth attacking based on current settings, False otherwise
    """

    try:
        logging.info(f"Is worth attacking based on resources: {int(mineral_value) > 800000}")
        result = is_worth_based_on_defences(screen_path)  # and int(mineral_value) > 800000
        logging.info(f"Is worth attacking: {result}")
        logging.info("---------------------------ended calculating, proceeds to next enemy---------------------------")

        return result
    except Exception as e:
        raise e


def is_worth_based_on_defences(screen_path):
    """
    Determines if a base is worth attacking based on defences recognized by model.

    Params:
        screen_path (str): Path to the screenshot image

    Returns:
        bool: True if the base is worth attacking, False otherwise
    """
    try:
        image = cv2.imread(screen_path)
        if image is None:
            raise FileNotFoundError(f"Image not found at {screen_path}")
        model_path = "../model/train104/weights/best.pt"
        model = YOLO(model_path)
        results = model(image)[0]
        result_path, image = save_detection_results(screen_path, results)
        base_coords, detections = parse_detection_file(result_path)
        deltas, is_base_on_edge = calculate_detections_deltas(detections, base_coords)
        if deltas:
            draw_encompassing_rectangle(image, tuple(deltas))
            cv2.imwrite(f"{screen_path}_detections.png", image)
        else:
            logging.error("No valid boxes found to calculate average location and deltas.")
            return False

        # worth attacking when base is on edge or there are less than 2 defensive buildings
        result = len(results.boxes.data) < 3 or is_base_on_edge
        logging.info(f"Is worth attacking based on defences: {result}")
        return result
    except Exception as e:
        raise e


def draw_encompassing_rectangle(image, deltas):
    """
    Draws an encompassing rectangle on the image based on delta values.

    Params:
        image: The image to draw on
        deltas (tuple of 4 floats): The delta values for the rectangle corners
    """
    try:
        delta_x1, delta_x2, delta_y1, delta_y2 = deltas
        cv2.rectangle(image, (int(delta_x1), int(delta_y1)), (int(delta_x2), int(delta_y2)), (255, 0, 0), 4)
    except Exception as e:
        raise e
