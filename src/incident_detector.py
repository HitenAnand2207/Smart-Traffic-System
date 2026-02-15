import numpy as np
from typing import List, Dict
import supervision as sv

class IncidentDetector:
    """
    Detect traffic incidents like accidents, vehicle breakdowns, and unusual behavior.
    """
    
    def __init__(self):
        self.vehicle_speeds = {}
        self.stalled_vehicles = {}  # tracker_id -> frame_count
        self.stopped_threshold = 1.0  # pixels/frame
        self.stopped_frames_threshold = 30  # ~1 second at 30fps
        self.incidents = []
        self.incident_history = []
        
    def update(self, detections: sv.Detections, speed_estimator=None):
        """
        Update incident detector with detections and speed data.
        """
        self.incidents = []
        
        # Check for stalled vehicles
        vehicle_positions = {}
        for tracker_id, box in zip(detections.tracker_id, detections.xyxy):
            if tracker_id is not None:
                center_x = (box[0] + box[2]) / 2
                center_y = (box[1] + box[3]) / 2
                vehicle_positions[tracker_id] = (center_x, center_y)
        
        # Update stalled vehicle tracking
        for tracker_id, pos in vehicle_positions.items():
            if tracker_id not in self.vehicle_speeds:
                self.vehicle_speeds[tracker_id] = []
            
            self.vehicle_speeds[tracker_id].append(pos)
            if len(self.vehicle_speeds[tracker_id]) > 120:  # Keep 2 seconds history
                self.vehicle_speeds[tracker_id].pop(0)
        
        # Access speed data if available
        if speed_estimator is not None:
            self._detect_stalled_vehicles(vehicle_positions, speed_estimator)
            self._detect_unusual_behavior(detections, speed_estimator)
        
        self.incident_history.extend(self.incidents)
        # Keep last 100 incidents
        if len(self.incident_history) > 100:
            self.incident_history = self.incident_history[-100:]
    
    def _detect_stalled_vehicles(self, vehicle_positions: Dict, speed_estimator):
        """
        Detect vehicles that are stopped in the middle of the road.
        """
        all_speeds = speed_estimator.get_all_speeds()
        
        for tracker_id, speed_info in all_speeds.items():
            if speed_info['speed_pf'] < 0.5:  # Very slow or stopped
                if tracker_id not in self.stalled_vehicles:
                    self.stalled_vehicles[tracker_id] = 0
                
                self.stalled_vehicles[tracker_id] += 1
                
                # Report incident if stalled too long
                if self.stalled_vehicles[tracker_id] > self.stopped_frames_threshold:
                    if tracker_id in vehicle_positions:
                        pos = vehicle_positions[tracker_id]
                        self.incidents.append({
                            'type': 'stalled_vehicle',
                            'tracker_id': tracker_id,
                            'position': pos,
                            'severity': 'high',
                            'duration_frames': self.stalled_vehicles[tracker_id]
                        })
            else:
                if tracker_id in self.stalled_vehicles:
                    del self.stalled_vehicles[tracker_id]
    
    def _detect_unusual_behavior(self, detections: sv.Detections, speed_estimator):
        """
        Detect unusual vehicle behavior (sudden stops, rapid acceleration, etc.).
        """
        all_speeds = speed_estimator.get_all_speeds()
        
        for tracker_id, speed_info in all_speeds.items():
            # Check for rapid speed changes
            if tracker_id in self.vehicle_speeds:
                history = self.vehicle_speeds[tracker_id]
                if len(history) >= 10:
                    # Calculate speed variance
                    positions = history[-10:]
                    distances = []
                    for i in range(1, len(positions)):
                        dx = positions[i][0] - positions[i-1][0]
                        dy = positions[i][1] - positions[i-1][1]
                        dist = np.sqrt(dx**2 + dy**2)
                        distances.append(dist)
                    
                    if distances:
                        variance = np.var(distances)
                        if variance > 50:  # High variance indicates erratic behavior
                            self.incidents.append({
                                'type': 'erratic_driving',
                                'tracker_id': tracker_id,
                                'position': history[-1] if history else (0, 0),
                                'severity': 'medium',
                                'variance': float(variance)
                            })
    
    def detect_accidents_from_detections(self, detections: sv.Detections) -> List[Dict]:
        """
        Simple accident detection based on spatial clustering of stationary boxes.
        More sophisticated approach would use optical flow, etc.
        """
        accidents = []
        
        if len(detections.xyxy) < 2:
            return accidents
        
        # Find overlapping/very close bounding boxes (potential collision/accident)
        boxes = detections.xyxy
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                iou = self._calculate_iou(boxes[i], boxes[j])
                
                # If boxes overlap significantly, potential accident
                if iou > 0.3:
                    accidents.append({
                        'type': 'potential_accident',
                        'vehicle_1_id': detections.tracker_id[i],
                        'vehicle_2_id': detections.tracker_id[j],
                        'overlap_ratio': float(iou),
                        'severity': 'high' if iou > 0.5 else 'medium',
                        'box_1': boxes[i].tolist(),
                        'box_2': boxes[j].tolist()
                    })
        
        return accidents
    
    def _calculate_iou(self, box1, box2) -> float:
        """
        Calculate Intersection over Union between two boxes.
        """
        x1_min, y1_min, x1_max, y1_max = box1
        x2_min, y2_min, x2_max, y2_max = box2
        
        # Intersection
        inter_xmin = max(x1_min, x2_min)
        inter_ymin = max(y1_min, y2_min)
        inter_xmax = min(x1_max, x2_max)
        inter_ymax = min(y1_max, y2_max)
        
        if inter_xmax < inter_xmin or inter_ymax < inter_ymin:
            return 0.0
        
        inter_area = (inter_xmax - inter_xmin) * (inter_ymax - inter_ymin)
        
        # Union
        box1_area = (x1_max - x1_min) * (y1_max - y1_min)
        box2_area = (x2_max - x2_min) * (y2_max - y2_min)
        union_area = box1_area + box2_area - inter_area
        
        return inter_area / union_area if union_area > 0 else 0
    
    def get_incidents(self) -> List[Dict]:
        """
        Get current incidents.
        """
        return self.incidents.copy()
    
    def get_incident_history(self) -> List[Dict]:
        """
        Get incident history.
        """
        return self.incident_history.copy()
    
    def get_incident_summary(self) -> Dict:
        """
        Get summary of incidents for dashboard.
        """
        current_incidents = self.incidents
        
        incident_counts = {}
        for incident in self.incident_history:
            incident_type = incident.get('type', 'unknown')
            incident_counts[incident_type] = incident_counts.get(incident_type, 0) + 1
        
        return {
            'total_current': len(current_incidents),
            'high_severity': len([i for i in current_incidents if i.get('severity') == 'high']),
            'incident_types': incident_counts,
            'latest_incidents': current_incidents[:5]
        }
