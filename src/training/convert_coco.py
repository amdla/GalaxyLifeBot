import json
import os


def convert_coco_to_yolo(coco_json_path, output_dir):
    """
    Converts COCO annotations to YOLO format.

    Parameters:
    coco_json_path (str): Path to the COCO JSON file.
    output_dir (str): Directory to save YOLO formatted labels.
    """
    with open(coco_json_path) as f:
        data = json.load(f)

    images = {img['id']: img for img in data['images']}
    annotations = data['annotations']

    os.makedirs(output_dir, exist_ok=True)

    for ann in annotations:
        img_id = ann['image_id']
        img = images[img_id]
        img_filename = img['file_name']
        img_width = img['width']
        img_height = img['height']
        category_id = ann['category_id']

        # YOLO format: <class_id> <x_center> <y_center> <width> <height>
        x, y, w, h = ann['bbox']
        x_center = x + w / 2
        y_center = y + h / 2
        yolo_bbox = [x_center / img_width, y_center / img_height, w / img_width, h / img_height]

        label_filename = os.path.splitext(img_filename)[0] + '.txt'
        label_file_path = os.path.join(output_dir, label_filename)

        with open(label_file_path, 'a') as label_file:
            label_file.write(f"{category_id} {' '.join(map(str, yolo_bbox))}\n")


if __name__ == "__main__":
    coco_json_path = '../../instances_default.json'
    output_dir = 'C:/Users/macie/PycharmProjects/GalaxyLifeBot/src/training/labels'
    convert_coco_to_yolo(coco_json_path, output_dir)
