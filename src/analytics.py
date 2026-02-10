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

    def update_analytics(self, detections):

        for tracker_id, class_id, box in zip(detections.tracker_id, detections.class_id, detections.xyxy):
            # Track count
            if tracker_id not in self.recorded_ids:
                class_name = self.get_class_name(class_id)
                if class_name in self.total_counts:
                    self.total_counts[class_name] += 1
                self.recorded_ids.add(tracker_id)

            # Track movement for risk
            center = [(box[0] + box[2]) / 2, (box[1] + box[3]) / 2]
            
            # Check for violation (e.g., crossing stop line)
            # Scaling center[1] by frame height (we'll assume normalized for now or pass height)
            # In a real app we pass frame dimensions
            self.check_violations(tracker_id, center, class_id)

            if tracker_id not in self.vehicle_history:
                self.vehicle_history[tracker_id] = []
            self.vehicle_history[tracker_id].append(center)
            
            # Keep only last 30 frames of history
            if len(self.vehicle_history[tracker_id]) > 30:
                self.vehicle_history[tracker_id].pop(0)

    def check_violations(self, tracker_id, center, class_id):
        # Dummy violation: crossing stop line when "RED"
        # We need to know signal state. Let's assume a state we pass or manage.
        pass

    def log_violation(self, tracker_id, v_type, class_id):
        event = {
            "tracker_id": tracker_id,
            "type": v_type,
            "class": self.get_class_name(class_id),
            "timestamp": "Now" # Placeholder
        }
        if event not in self.violation_logs:
            self.violation_logs.append(event)

    def calculate_risk_index(self):
        """
        Simple risk index based on number of active vehicles and their erratic movement (if any).
        """
        if not self.vehicle_history:
            return 0.0
        
        # Base risk from density
        active_vehicles = len(self.vehicle_history)
        risk = active_vehicles * 5.0  # arbitrary scaling
        
        # Add risk for "fast" movements (delta distance between frames)
        # This is a proxy for speed since we don't have calibrated pixels-to-meters
        # But we can detect outliers
        return min(risk, 100.0)

    def estimate_emissions(self):
        """
        Estimate CO2 emissions based on current vehicle counts.
        """
        total_co2 = 0
        for v_type, count in self.total_counts.items():
            factor = config.EMISSION_FACTORS.get(v_type, 0)
            total_co2 += (count * factor) / 60.0 # g/sec approximate
        return total_co2

    def get_signal_recommendation(self):
        """
        Recommend signal time based on current vehicle count (Queue length proxy).
        """
        active_vehicles = len(self.vehicle_history)
        if active_vehicles > 15:
            return "High Traffic: Increase Green by 15s"
        elif active_vehicles > 5:
            return "Moderate Traffic: Increase Green by 5s"
        else:
            return "Low Traffic: Maintain Standard Timing"

    def get_class_name(self, class_id):
        # Mapping COCO IDs to our config names
        mapping = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck", 1: "bicycle"}
        return mapping.get(int(class_id), "unknown")
