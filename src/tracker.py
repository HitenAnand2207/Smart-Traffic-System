import supervision as sv
import numpy as np

class TrafficTracker:
    def __init__(self):
        """
        Initialize the ByteTrack tracker from Supervision.
        """
        self.tracker = sv.ByteTrack()
        self.box_annotator = sv.BoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()
        self.trace_annotator = sv.TraceAnnotator()

    def update(self, detections: sv.Detections):
        """
        Update tracker with new detections.
        """
        # ByteTrack update
        detections = self.tracker.update_with_detections(detections)
        return detections

    def annotate_frame(self, frame, detections: sv.Detections):
        """
        Annotate the frame with bounding boxes, labels, and traces.
        """
        labels = [
            f"#{tracker_id} {class_name} {confidence:.2f}"
            for tracker_id, class_name, confidence in zip(
                detections.tracker_id,
                detections.data['class_name'],
                detections.confidence
            )
        ]
        
        annotated_frame = frame.copy()
        annotated_frame = self.trace_annotator.annotate(scene=annotated_frame, detections=detections)
        annotated_frame = self.box_annotator.annotate(scene=annotated_frame, detections=detections)
        annotated_frame = self.label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
        
        return annotated_frame
