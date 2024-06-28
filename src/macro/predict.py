import os

import cv2
from ultralytics import YOLO

from utils import handle_error


def parse_detection_file(result_path):
    try:
        with open(result_path, 'r') as file:
            lines = file.readlines()

        base_coords = None
        detections = []

        for line in lines:
            parts = line.strip().split(',')
            if len(parts) == 6:
                class_id, score, x1, y1, x2, y2 = map(float, parts)
                if class_id == 7.0:
                    base_coords = (x1, y1, x2, y2)
                detections.append((x1, y1, x2, y2))

        return base_coords, detections
    except Exception as e:
        print(f"Error: {e}")
        handle_error()


def calculate_average_location_and_deltas(detections, base_coords):
    try:
        if not detections or base_coords is None:
            return None, None, None, None, None, None, None

        avg_coords = [((x1 + x2) / 2, (y1 + y2) / 2) for x1, y1, x2, y2 in detections]

        total_avg_x = sum(coord[0] for coord in avg_coords) / len(avg_coords)
        total_avg_y = sum(coord[1] for coord in avg_coords) / len(avg_coords)

        x1_values = [coords[0] for coords in detections]
        x2_values = [coords[2] for coords in detections]
        y1_values = [coords[1] for coords in detections]
        y2_values = [coords[3] for coords in detections]

        delta_x1 = min(x1_values)
        delta_x2 = max(x2_values)
        delta_y1 = min(y1_values)
        delta_y2 = max(y2_values)

        is_base_on_edge = (base_coords and
                           (base_coords[0] == delta_x1 or base_coords[2] == delta_x2 or
                            base_coords[1] == delta_y1 or base_coords[3] == delta_y2))

        return total_avg_x, total_avg_y, delta_x1, delta_x2, delta_y1, delta_y2, is_base_on_edge
    except Exception as e:
        print(f"Error: {e}")
        handle_error()


def save_detection_results(screen_path, results):
    try:
        result_path = f"{screen_path}.txt"
        image = cv2.imread(screen_path)

        with open(result_path, 'w') as f:
            f.write(f"Total detected boxes: {len(results.boxes.data)}\n")
            f.write("Detected boxes and their scores:\n")
            for result in results.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = result
                f.write(f"{class_id},{score},{x1},{y1},{x2},{y2}\n")
                if score > 0.33:
                    cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                    cv2.putText(image, results.names[int(class_id)].upper(), (int(x1), int(y1) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 2, cv2.LINE_AA)

        return result_path, image
    except Exception as e:
        print(f"Error: {e}")
        handle_error()


def draw_encompassing_rectangle(image, deltas):
    try:
        delta_x1, delta_x2, delta_y1, delta_y2 = deltas
        cv2.rectangle(image, (int(delta_x1), int(delta_y1)), (int(delta_x2), int(delta_y2)), (255, 0, 0), 4)
    except Exception as e:
        print(f"Error: {e}")
        handle_error()


def is_worth_based_on_defences(screen_path):
    try:
        image = cv2.imread(screen_path)
        if image is None:
            raise FileNotFoundError(f"Image not found at {screen_path}")

        model_path = os.path.join('C:\\', 'Users', 'macie', 'PycharmProjects', 'GalaxyLifeBot', 'src', 'runs', 'detect',
                                  'train104', 'weights', 'best.pt')
        model = YOLO(model_path)

        results = model(image)[0]
        result_path, image = save_detection_results(screen_path, results)

        base_coords, detections = parse_detection_file(result_path)
        total_avg_x, total_avg_y, delta_x1, delta_x2, delta_y1, delta_y2, is_base_on_edge = calculate_average_location_and_deltas(
            detections, base_coords)

        if total_avg_x is not None and total_avg_y is not None:
            draw_encompassing_rectangle(image, (delta_x1, delta_x2, delta_y1, delta_y2))
            cv2.imwrite(f"{screen_path}_detections.png", image)
        else:
            print("No valid boxes found to calculate average location and deltas.")
            return False

        result = is_base_on_edge or len(results.boxes.data) < 6
        print(f"Is worth attacking based on defences: {result}")
        return result
    except Exception as e:
        print(f"Error: {e}")
        handle_error()
