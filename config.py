import os

# Model Settings
MODEL_PATH = os.path.join("models", "yolov8n.pt")
CONFIDENCE_THRESHOLD = 0.3
IOU_THRESHOLD = 0.45

# Vehicle Classes (COCO indices for YOLOv8)
# 2: car, 3: motorcycle, 5: bus, 7: truck, 1: bicycle
VEHICLE_CLASSES = [2, 3, 5, 7, 1]

# Analytics Settings
EMISSION_FACTORS = {
    "car": 120.0,       # g CO2 / min idling (example)
    "bus": 450.0,
    "truck": 500.0,
    "motorcycle": 60.0,
    "bicycle": 0.0
}

# UI Settings
DASHBOARD_TITLE = "Smart Traffic Analytics System"
LOG_DIR = os.path.join("data", "logs")

# Violation Areas (Normalized coordinates [x, y])
# These will be set via the UI in a real app, but we'll define defaults
STOP_LINE_Y = 0.7  # 70% down the frame
