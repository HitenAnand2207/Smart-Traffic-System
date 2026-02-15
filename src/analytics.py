import numpy as np
import config

class TrafficAnalytics:
    def __init__(self):
        self.vehicle_history = {} 
        self.violation_logs = []
        self.total_counts = {
            "car": 0, "bus": 0, "truck": 0, "motorcycle": 0, "bicycle": 0
        }
        self.recorded_ids = set()
        self.frame_count = 0
        self.start_time = None
        self.peak_vehicles = 0
        self.average_vehicles = []

    def update_analytics(self, detections, frame_time: float = None):
        """
        Update analytics with current detections.
        """
        self.frame_count += 1
        
        current_vehicle_count = 0
        for tracker_id, class_id, box in zip(detections.tracker_id, detections.class_id, detections.xyxy):
            current_vehicle_count += 1
            
            # Track count
            if tracker_id not in self.recorded_ids:
                class_name = self.get_class_name(class_id)
                if class_name in self.total_counts:
                    self.total_counts[class_name] += 1
                self.recorded_ids.add(tracker_id)

            # Track movement for risk
            center = [(box[0] + box[2]) / 2, (box[1] + box[3]) / 2]
            
            # Check for violation (e.g., crossing stop line)
            self.check_violations(tracker_id, center, class_id)

            if tracker_id not in self.vehicle_history:
                self.vehicle_history[tracker_id] = []
            self.vehicle_history[tracker_id].append(center)
            
            # Keep only last 30 frames of history
            if len(self.vehicle_history[tracker_id]) > 30:
                self.vehicle_history[tracker_id].pop(0)
        
        # Track statistics
        self.average_vehicles.append(current_vehicle_count)
        if len(self.average_vehicles) > 300:  # Keep 10 seconds at 30fps
            self.average_vehicles.pop(0)
        
        if current_vehicle_count > self.peak_vehicles:
            self.peak_vehicles = current_vehicle_count

    def check_violations(self, tracker_id, center, class_id):
        """
        Check for traffic violations (e.g., crossing stop line when RED).
        """
        # Dummy violation detection - can be extended with actual rules
        # For now, we'll check if vehicles cross predefined stop lines
        stop_line_y = config.STOP_LINE_Y
        
        if center[1] > stop_line_y * 0.95:  # Close to or past stop line
            # Check if this is a new violation (not already logged)
            if tracker_id not in self.recorded_ids or self.vehicle_history[tracker_id][-1][1] > stop_line_y:
                self.log_violation(tracker_id, "crossing_stop_line", class_id)

    def log_violation(self, tracker_id, v_type, class_id):
        """
        Log a traffic violation.
        """
        event = {
            "tracker_id": tracker_id,
            "type": v_type,
            "class": self.get_class_name(class_id),
            "timestamp": self.frame_count
        }
        if event not in self.violation_logs:
            self.violation_logs.append(event)
            # Keep only last 50 violations
            if len(self.violation_logs) > 50:
                self.violation_logs.pop(0)

    def calculate_risk_index(self):
        """
        Calculate comprehensive risk index based on multiple factors.
        """
        if not self.vehicle_history:
            return 0.0
        
        # Base risk from density
        active_vehicles = len(self.vehicle_history)
        risk = active_vehicles * 3.0
        
        # Add risk for violations
        risk += len([v for v in self.violation_logs[-30:] if v['type'] == 'crossing_stop_line']) * 5.0
        
        # Add risk for erratic movements
        erratic_count = 0
        for traj in self.vehicle_history.values():
            if len(traj) > 3:
                distances = []
                for i in range(1, len(traj)):
                    dx = traj[i][0] - traj[i-1][0]
                    dy = traj[i][1] - traj[i-1][1]
                    distances.append(np.sqrt(dx**2 + dy**2))
                
                if np.std(distances) > 20:  # High variance in movement
                    erratic_count += 1
        
        risk += erratic_count * 8.0
        
        return min(risk, 100.0)

    def estimate_emissions(self):
        """
        Estimate CO2 emissions based on current vehicle counts and activity.
        """
        total_co2 = 0
        for v_type, count in self.total_counts.items():
            factor = config.EMISSION_FACTORS.get(v_type, 0)
            total_co2 += (count * factor) / 60.0  # g/sec approximate
        return total_co2

    def get_signal_recommendation(self):
        """
        Recommend signal time based on current vehicle count and traffic flow.
        """
        active_vehicles = len(self.vehicle_history)
        avg_vehicles = np.mean(self.average_vehicles[-30:]) if self.average_vehicles else 0
        
        if active_vehicles > avg_vehicles * 1.5 and active_vehicles > 15:
            return "🔴 High Traffic: Extend Green by 20s"
        elif active_vehicles > avg_vehicles * 1.2 and active_vehicles > 8:
            return "🟡 Moderate Traffic: Extend Green by 10s"
        elif active_vehicles > avg_vehicles * 0.8:
            return "🟢 Light Traffic: Maintain Normal Timing"
        else:
            return "🟢 Very Light: Reduce Green by 5s"

    def get_class_name(self, class_id):
        """
        Mapping COCO IDs to class names.
        """
        mapping = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck", 1: "bicycle"}
        return mapping.get(int(class_id), "unknown")
    
    def get_statistics(self):
        """
        Get comprehensive traffic statistics.
        """
        return {
            'total_vehicles_detected': sum(self.total_counts.values()),
            'vehicle_counts': self.total_counts.copy(),
            'peak_vehicles': self.peak_vehicles,
            'current_vehicles': len(self.vehicle_history),
            'average_vehicles': float(np.mean(self.average_vehicles)) if self.average_vehicles else 0,
            'violations': len(self.violation_logs),
            'frames_processed': self.frame_count,
            'risk_index': self.calculate_risk_index(),
            'emissions': self.estimate_emissions()
        }
