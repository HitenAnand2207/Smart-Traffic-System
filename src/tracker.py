import supervision as sv
import numpy as np
import cv2

class TrafficTracker:
    def __init__(self, trace_length: int = 30):
        """
        Initialize the ByteTrack tracker from Supervision with enhanced features.
        
        Args:
            trace_length: Length of trace history to maintain
        """
        self.tracker = sv.ByteTrack()
        self.box_annotator = sv.BoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()
        self.trace_annotator = sv.TraceAnnotator(trace_length=trace_length)
        self.trajectory_history = {}  # tracker_id -> list of centroids
        self.frame_count = 0

    def update(self, detections: sv.Detections):
        """
        Update tracker with new detections and maintain trajectory history.
        """
        # ByteTrack update
        detections = self.tracker.update_with_detections(detections)
        
        # Update trajectory history
        for tracker_id, box in zip(detections.tracker_id, detections.xyxy):
            if tracker_id is not None:
                center_x = (box[0] + box[2]) / 2
                center_y = (box[1] + box[3]) / 2
                
                if tracker_id not in self.trajectory_history:
                    self.trajectory_history[tracker_id] = []
                
                self.trajectory_history[tracker_id].append((center_x, center_y))
                
                # Keep only last 120 frames (4 seconds at 30fps)
                if len(self.trajectory_history[tracker_id]) > 120:
                    self.trajectory_history[tracker_id].pop(0)
        
        # Clean up lost tracks
        active_ids = set(detections.tracker_id)
        self.trajectory_history = {k: v for k, v in self.trajectory_history.items() if k in active_ids}
        
        self.frame_count += 1
        return detections

    def annotate_frame(self, frame, detections: sv.Detections, show_trajectory: bool = True):
        """
        Annotate the frame with bounding boxes, labels, and traces.
        
        Args:
            frame: Original frame
            detections: Detections with tracker IDs
            show_trajectory: Whether to draw trajectory lines
        """
        labels = [
            f"#{tracker_id} {class_name} {confidence:.2f}"
            for tracker_id, class_name, confidence in zip(
                detections.tracker_id,
                detections.data.get('class_name', ['unknown'] * len(detections.tracker_id)),
                detections.confidence
            )
        ]
        
        annotated_frame = frame.copy()
        annotated_frame = self.trace_annotator.annotate(scene=annotated_frame, detections=detections)
        annotated_frame = self.box_annotator.annotate(scene=annotated_frame, detections=detections)
        annotated_frame = self.label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
        
        # Draw detailed trajectories if requested
        if show_trajectory:
            annotated_frame = self._draw_trajectories(annotated_frame)
        
        return annotated_frame
    
    def _draw_trajectories(self, frame: np.ndarray) -> np.ndarray:
        """
        Draw trajectory trails for all tracked vehicles.
        """
        annotated = frame.copy()
        
        for tracker_id, trajectory in self.trajectory_history.items():
            if len(trajectory) > 1:
                # Convert to numpy array for polylines
                points = np.array(trajectory, dtype=np.int32).reshape((-1, 1, 2))
                
                # Draw trajectory with fading effect
                for i in range(1, len(points)):
                    # Fade factor - older points are more transparent
                    alpha = i / len(points)
                    color = (int(100 * alpha), int(255 * alpha), int(150 * alpha))
                    cv2.line(annotated, tuple(points[i-1][0]), tuple(points[i][0]), color, 2)
        
        return annotated
    
    def get_trajectory(self, tracker_id):
        """
        Get trajectory for a specific vehicle.
        """
        return self.trajectory_history.get(tracker_id, [])
    
    def get_all_trajectories(self):
        """
        Get all vehicle trajectories.
        """
        return self.trajectory_history.copy()
