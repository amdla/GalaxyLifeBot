import os

from ultralytics import YOLO

# Enable more detailed CUDA error reporting
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
os.environ['CUDA_VISIBLE_DEVICES'] = "0"  # Adjust if using multiple GPUs

if __name__ == "__main__":
    # Load a model
    model = YOLO("yolov8l.yaml")  # build a new model from scratch

    # Use the model
    model.train(data="config.yaml", epochs=200)  # train the model
