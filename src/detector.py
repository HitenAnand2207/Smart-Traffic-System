import cv2
from ultralytics import YOLO
import config

class TrafficDetector:
    def __init__(self, model_path=config.MODEL_PATH):
        """
        Initialize the YOLOv8 detector.
        """
        self.model = YOLO(model_path)
        self.classes = config.VEHICLE_CLASSES
        self.conf = config.CONFIDENCE_THRESHOLD
        self.iou = config.IOU_THRESHOLD

    def detect(self, frame):
        """
        Run detection on a single frame.
        Yields detections filtered by vehicle classes.
        """
        results = self.model.predict(
            source=frame,
            conf=self.conf,
            iou=self.iou,
            classes=self.classes,
            verbose=False
        )
        return results[0]

    def get_class_name(self, class_id):
        """
        Helper to get class name from ID.
        """
        return self.model.names[int(class_id)]
