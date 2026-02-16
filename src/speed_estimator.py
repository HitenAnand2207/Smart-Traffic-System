import numpy as np
import cv2
from typing import Dict, Tuple, List
import supervision as sv

class SpeedEstimator:
    """
    Vehicle speed and direction estimation using multi-frame tracking.
    Provides calibrated speed estimates in pixels/frame and optional m/s with calibration.
    """
    
    def __init__(self, fps: int = 30, pixels_per_meter: float = 50.0):
        """
        Initialize speed estimator.
        
        Args:
            fps: Frames per second of video
            pixels_per_meter: Calibration factor (pixels per real-world meter)
        """
        self.fps = fps
        self.pixels_per_meter = pixels_per_meter
        self.frame_time = 1.0 / fps
        self.vehicle_trajectories = {}  # tracker_id -> list of (x, y, frame_num)
        self.vehicle_speeds = {}  # tracker_id -> speed info
        self.frame_count = 0
        
    def update(self, detections: sv.Detections):
        """
        Update speed estimator with new detections.
        
        Args:
            detections: Current frame detections with tracker IDs
        """
        self.frame_count += 1
        current_positions = {}
        
        # Extract centers from boxes
        for i, (box, tracker_id) in enumerate(zip(detections.xyxy, detections.tracker_id)):
            # Skip if tracker_id is None
            if tracker_id is None:
                continue
            if tracker_id not in current_positions:  # Keep first detection if duplicate tracking IDs
                center_x = (box[0] + box[2]) / 2
                center_y = (box[1] + box[3]) / 2
                current_positions[tracker_id] = (center_x, center_y, box)
        
        # Update trajectories and calculate speeds
        for tracker_id, pos in current_positions.items():
            if tracker_id not in self.vehicle_trajectories:
                self.vehicle_trajectories[tracker_id] = []
            
            self.vehicle_trajectories[tracker_id].append({
                'pos': pos[:2],
                'box': pos[2],
                'frame': self.frame_count
            })
            
            # Keep only last 60 frames (2 seconds at 30fps)
            if len(self.vehicle_trajectories[tracker_id]) > 60:
                self.vehicle_trajectories[tracker_id].pop(0)
            
            # Calculate speed if enough history
            if len(self.vehicle_trajectories[tracker_id]) >= 3:
                self.vehicle_speeds[tracker_id] = self._calculate_speed(
                    self.vehicle_trajectories[tracker_id]
                )
        
        # Clean up lost vehicles
        self.vehicle_trajectories = {
            k: v for k, v in self.vehicle_trajectories.items() if k in current_positions
        }
    
    def _calculate_speed(self, trajectory: List[Dict]) -> Dict:
        """
        Calculate speed from trajectory.
        
        Args:
            trajectory: List of position dictionaries
            
        Returns:
            Speed information dictionary
        """
        recent = trajectory[-10:] if len(trajectory) >= 10 else trajectory
        
        distances = []
        for i in range(1, len(recent)):
            x1, y1 = recent[i-1]['pos']
            x2, y2 = recent[i]['pos']
            distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
            distances.append(distance)
        
        if not distances:
            return {'speed_pf': 0, 'speed_ms': 0, 'direction': 0, 'stability': 0}
        
        # Average speed in pixels per frame
        speed_pf = np.mean(distances)
        speed_ms = speed_pf / self.pixels_per_meter * self.fps
        
        # Direction
        dx = recent[-1]['pos'][0] - recent[0]['pos'][0]
        dy = recent[-1]['pos'][1] - recent[0]['pos'][1]
        direction_rad = np.arctan2(dy, dx)
        direction_deg = np.degrees(direction_rad)
        
        # Speed stability (lower std = more stable)
        stability = 1.0 - min(np.std(distances) / (speed_pf + 0.1), 1.0)
        
        return {
            'speed_pf': float(speed_pf),
            'speed_ms': float(speed_ms),
            'direction_deg': float(direction_deg),
            'direction_rad': float(direction_rad),
            'stability': float(stability),
            'samples': len(recent)
        }
    
    def get_vehicle_speed(self, tracker_id: int) -> Dict:
        """
        Get speed information for a specific vehicle.
        """
        return self.vehicle_speeds.get(tracker_id, {
            'speed_pf': 0,
            'speed_ms': 0,
            'direction_deg': 0,
            'stability': 0
        })
    
    def get_all_speeds(self) -> Dict[int, Dict]:
        """
        Get speeds for all tracked vehicles.
        """
        return self.vehicle_speeds.copy()
    
    def get_average_speed(self) -> float:
        """
        Get average speed of all vehicles (m/s).
        """
        if not self.vehicle_speeds:
            return 0.0
        speeds = [v['speed_ms'] for v in self.vehicle_speeds.values()]
        return float(np.mean(speeds))
    
    def get_speed_histogram(self) -> Dict:
        """
        Get histogram of vehicle speeds for analytics.
        """
        if not self.vehicle_speeds:
            return {'bins': [], 'counts': [], 'mean': 0, 'max': 0}
        
        speeds = [v['speed_ms'] for v in self.vehicle_speeds.values()]
        
        hist, bins = np.histogram(speeds, bins=10, range=(0, max(speeds) + 1))
        
        return {
            'bins': bins.tolist(),
            'counts': hist.tolist(),
            'mean': float(np.mean(speeds)),
            'max': float(np.max(speeds)),
            'min': float(np.min(speeds)),
            'std': float(np.std(speeds))
        }
    
    def draw_speed_annotations(self, frame: np.ndarray, detections: sv.Detections) -> np.ndarray:
        """
        Draw speed vectors and direction on frame.
        """
        annotated = frame.copy()
        
        for tracker_id, box in zip(detections.tracker_id, detections.xyxy):
            if tracker_id is None or tracker_id not in self.vehicle_speeds:
                continue
            
            speed_info = self.vehicle_speeds[tracker_id]
            center_x = int((box[0] + box[2]) / 2)
            center_y = int((box[1] + box[3]) / 2)
            
            # Draw speed vector
            if speed_info['speed_pf'] > 0.5:
                length = min(int(speed_info['speed_pf'] * 10), 50)
                end_x = int(center_x + length * np.cos(speed_info['direction_rad']))
                end_y = int(center_y + length * np.sin(speed_info['direction_rad']))
                
                cv2.arrowedLine(annotated, (center_x, center_y), (end_x, end_y),
                               (0, 255, 0), 2, tipLength=0.3)
            
            # Draw speed text
            speed_text = f"{speed_info['speed_ms']:.1f} m/s"
            cv2.putText(annotated, speed_text,
                       (center_x - 20, center_y - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return annotated
    
    def calibrate_pixels_to_meters(self, known_distance_pixels: float, known_distance_meters: float):
        """
        Calibrate the pixel-to-meter conversion factor.
        
        Args:
            known_distance_pixels: Distance in pixels (measured from frame)
            known_distance_meters: Actual distance in meters
        """
        if known_distance_pixels > 0:
            self.pixels_per_meter = known_distance_pixels / known_distance_meters
