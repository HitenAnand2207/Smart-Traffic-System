# 🔧 Advanced API Reference & Developer Guide

## Complete API Documentation

### 1. CollisionDetector

Detects potential collisions between vehicles using trajectory analysis and collision risk scoring.

#### Initialization
```python
from src.collision_detector import CollisionDetector

# Default initialization
detector = CollisionDetector()

# With custom frame dimensions
detector = CollisionDetector(frame_width=1280, frame_height=720)
```

#### Methods

##### `update(detections, frame_time)`
Update collision detector with new detections.

**Parameters:**
- `detections` (sv.Detections): Detections with tracker IDs
- `frame_time` (float): Current timestamp

**Returns:** None

```python
detector.update(detections, current_time)
```

##### `get_alerts()`
Get current collision alerts sorted by risk score.

**Returns:** List[Dict]
```python
alerts = detector.get_alerts()
# Output:
# [
#   {
#     'vehicle_1': 0,
#     'vehicle_2': 5,
#     'risk_score': 0.85,
#     'position_1': (640, 360),
#     'position_2': (680, 380),
#     'distance': 50.2
#   }
# ]
```

##### `draw_collision_warnings(frame, detections)`
Draw collision warnings on frame.

**Parameters:**
- `frame` (np.ndarray): Input frame
- `detections` (sv.Detections): Current detections

**Returns:** np.ndarray - Annotated frame

```python
annotated = detector.draw_collision_warnings(frame, detections)
```

#### Attributes
- `safety_distance` (int): Minimum safe distance in pixels (default: 50)
- `vehicle_trajectories` (Dict): Trajectory history for each vehicle
- `collision_alerts` (List): Current collision alerts

---

### 2. TrafficPredictor

Predicts future traffic patterns and detects anomalies using time-series analysis.

#### Initialization
```python
from src.traffic_predictor import TrafficPredictor

# Default (60 frame history, 30 frame prediction)
predictor = TrafficPredictor()

# Custom configuration
predictor = TrafficPredictor(history_length=120, prediction_horizon=60)
```

#### Methods

##### `update(vehicle_count, average_speed, congestion_level, timestamp)`
Update predictor with current metrics.

**Parameters:**
- `vehicle_count` (int): Number of vehicles
- `average_speed` (float): Average speed (pixels/frame)
- `congestion_level` (float): Congestion 0-1
- `timestamp` (float): Current timestamp

```python
predictor.update(
    vehicle_count=12,
    average_speed=5.5,
    congestion_level=0.6,
    timestamp=current_time
)
```

##### `get_congestion_forecast()`
Get congestion forecast for future frames.

**Returns:** Dict
```python
forecast = predictor.get_congestion_forecast()
# Output:
# {
#   'status': 'Moderate Congestion Building',
#   'risk_level': 'Medium',
#   'current_congestion': 0.45,
#   'predicted_peak': 0.72,
#   'predictions': [0.48, 0.51, 0.55, ...],
#   'trend': 0.05
# }
```

##### `get_vehicle_count_forecast()`
Get vehicle count forecast.

**Returns:** Dict
```python
forecast = predictor.get_vehicle_count_forecast()
```

##### `get_anomaly_detection()`
Detect unusual traffic patterns.

**Returns:** Dict
```python
anomalies = predictor.get_anomaly_detection()
# Output:
# {
#   'anomalies': [
#     {
#       'type': 'unusual_vehicle_count',
#       'severity': 'high',
#       'z_score': 3.2
#     }
#   ],
#   'count': 1,
#   'alert': True
# }
```

---

### 3. SpeedEstimator

Estimates vehicle speeds and directions using multi-frame trajectory analysis.

#### Initialization
```python
from src.speed_estimator import SpeedEstimator

# Default (30 FPS, 50 pixels/meter)
estimator = SpeedEstimator()

# Custom configuration
estimator = SpeedEstimator(fps=60, pixels_per_meter=100.0)
```

#### Methods

##### `update(detections)`
Update speed estimator with new detections.

**Parameters:**
- `detections` (sv.Detections): Current frame detections

```python
estimator.update(detections)
```

##### `get_vehicle_speed(tracker_id)`
Get speed information for specific vehicle.

**Parameters:**
- `tracker_id` (int): Vehicle tracker ID

**Returns:** Dict
```python
speed_info = estimator.get_vehicle_speed(0)
# Output:
# {
#   'speed_pf': 8.5,  # pixels/frame
#   'speed_ms': 7.2,  # meters/second
#   'direction_deg': 45.0,  # degrees
#   'direction_rad': 0.785,  # radians
#   'stability': 0.92,  # 0-1, higher is more stable
#   'samples': 10  # number of frames used
# }
```

##### `get_all_speeds()`
Get speeds for all tracked vehicles.

**Returns:** Dict[int, Dict]

##### `get_average_speed()`
Get average speed of all vehicles.

**Returns:** float (m/s)

##### `get_speed_histogram()`
Get histogram of speed distribution.

**Returns:** Dict
```python
hist = estimator.get_speed_histogram()
# Output:
# {
#   'bins': [0, 1.5, 3.0, 4.5, ...],
#   'counts': [5, 12, 18, 10, ...],
#   'mean': 7.5,
#   'max': 15.2,
#   'min': 0.5,
#   'std': 3.2
# }
```

##### `draw_speed_annotations(frame, detections)`
Draw speed vectors on frame.

**Returns:** np.ndarray

##### `calibrate_pixels_to_meters(pixels, meters)`
Calibrate pixel-to-meter conversion.

**Parameters:**
- `known_distance_pixels` (float): Distance in pixels
- `known_distance_meters` (float): Actual distance in meters

```python
# If you measure 500 pixels = 25 meters
estimator.calibrate_pixels_to_meters(500, 25)
```

---

### 4. IncidentDetector

Detects traffic incidents like accidents, stalled vehicles, and abnormal behavior.

#### Initialization
```python
from src.incident_detector import IncidentDetector

detector = IncidentDetector()
```

#### Methods

##### `update(detections, speed_estimator)`
Update incident detector.

**Parameters:**
- `detections` (sv.Detections): Current detections
- `speed_estimator` (SpeedEstimator): Speed estimator instance

```python
detector.update(detections, speed_estimator)
```

##### `get_incidents()`
Get current incidents.

**Returns:** List[Dict]
```python
incidents = detector.get_incidents()
# Output:
# [
#   {
#     'type': 'stalled_vehicle',
#     'tracker_id': 3,
#     'position': (640, 480),
#     'severity': 'high',
#     'duration_frames': 45
#   }
# ]
```

##### `get_incident_history()`
Get historical incidents (last 100).

**Returns:** List[Dict]

##### `get_incident_summary()`
Get summary statistics.

**Returns:** Dict
```python
summary = detector.get_incident_summary()
# Output:
# {
#   'total_current': 2,
#   'high_severity': 1,
#   'incident_types': {
#     'stalled_vehicle': 5,
#     'erratic_driving': 2,
#     'potential_accident': 1
#   },
#   'latest_incidents': [...]
# }
```

#### Incident Types
- `stalled_vehicle`: Vehicle stopped in traffic
- `erratic_driving`: Unusual acceleration/deceleration
- `potential_accident`: Overlapping vehicles

---

### 5. HeatmapGenerator

Generates traffic density heatmaps and identifies congestion hotspots.

#### Initialization
```python
from src.heatmap_generator import HeatmapGenerator

# Default (1280x720, 32px grid)
generator = HeatmapGenerator()

# Custom
generator = HeatmapGenerator(frame_width=1920, frame_height=1080, grid_size=40)
```

#### Methods

##### `update(detections)`
Update heatmap with current detections.

```python
generator.update(detections)
```

##### `get_density_heatmap()`
Get current density heatmap.

**Returns:** Tuple[np.ndarray, np.ndarray]
```python
heatmap, smoothed = generator.get_density_heatmap()
# heatmap: Raw density 0-1
# smoothed: Gaussian-blurred version
```

##### `get_temporal_heatmap()`
Get accumulated heatmap over time.

**Returns:** np.ndarray (0-1)

##### `render_heatmap_on_frame(frame, use_temporal=False)`
Overlay heatmap on video frame.

**Parameters:**
- `frame` (np.ndarray): Input frame
- `use_temporal` (bool): Use temporal or current density

**Returns:** np.ndarray - Frame with heatmap overlay

```python
display_frame = generator.render_heatmap_on_frame(frame, use_temporal=False)
```

##### `get_hotspots(threshold=0.5)`
Identify high-density traffic zones.

**Returns:** List[Dict]
```python
hotspots = generator.get_hotspots(threshold=0.6)
# Output:
# [
#   {
#     'grid_x': 5,
#     'grid_y': 8,
#     'pixel_x': 160,
#     'pixel_y': 256,
#     'density': 0.85,
#     'box': (160, 256, 192, 288)
#   }
# ]
```

##### `get_congestion_index_by_region()`
Get congestion for 9 frame regions (3x3 grid).

**Returns:** Dict
```python
regions = generator.get_congestion_index_by_region()
# Output:
# {
#   'top_left': 0.2,
#   'top_center': 0.3,
#   'top_right': 0.1,
#   'mid_left': 0.4,
#   'mid_center': 0.8,
#   'mid_right': 0.3,
#   'bottom_left': 0.2,
#   'bottom_center': 0.5,
#   'bottom_right': 0.1
# }
```

##### `reset()`
Clear all heatmap data.

##### `draw_grid_overlay(frame, show_numbers=False)`
Draw reference grid on frame.

**Returns:** np.ndarray

---

### 6. TrafficTracker (Enhanced)

Enhanced tracking with trajectory history.

#### Methods

##### `get_trajectory(tracker_id)`
Get trajectory for specific vehicle.

**Returns:** List[Tuple[float, float]]

##### `get_all_trajectories()`
Get all vehicle trajectories.

**Returns:** Dict[int, List]

---

### 7. TrafficAnalytics (Enhanced)

Enhanced analytics module.

#### Methods

##### `get_statistics()`
Get comprehensive traffic statistics.

**Returns:** Dict
```python
stats = analytics.get_statistics()
# Output:
# {
#   'total_vehicles_detected': 450,
#   'vehicle_counts': {'car': 350, 'bus': 50, ...},
#   'peak_vehicles': 45,
#   'current_vehicles': 28,
#   'average_vehicles': 20.5,
#   'violations': 8,
#   'frames_processed': 1200,
#   'risk_index': 35.7,
#   'emissions': 125.3
# }
```

---

## Integration Example

```python
import cv2
import supervision as sv
from src.detector import TrafficDetector
from src.tracker import TrafficTracker
from src.collision_detector import CollisionDetector
from src.traffic_predictor import TrafficPredictor
from src.speed_estimator import SpeedEstimator
from src.incident_detector import IncidentDetector
from src.heatmap_generator import HeatmapGenerator

# Initialize
detector = TrafficDetector()
tracker = TrafficTracker()
collision_det = CollisionDetector()
predictor = TrafficPredictor()
speed_est = SpeedEstimator()
incident_det = IncidentDetector()
heatmap = HeatmapGenerator()

# Process video
cap = cv2.VideoCapture("traffic.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1
    timestamp = frame_count / fps
    
    # Detect
    results = detector.detect(frame)
    detections = sv.Detections.from_ultralytics(results)
    detections.data['class_name'] = [
        detector.get_class_name(c) for c in detections.class_id
    ]
    
    # Track
    detections = tracker.update(detections)
    
    # Analyze
    speed_est.update(detections)
    collision_det.update(detections, timestamp)
    incident_det.update(detections, speed_est)
    predictor.update(
        len(detections),
        speed_est.get_average_speed(),
        min(len(detections) / 20, 1.0),
        timestamp
    )
    heatmap.update(detections)
    
    # Get results
    collisions = collision_det.get_alerts()
    incidents = incident_det.get_incidents()
    forecast = predictor.get_congestion_forecast()
    hotspots = heatmap.get_hotspots()
    
    # Visualize
    frame = tracker.annotate_frame(frame, detections)
    frame = speed_est.draw_speed_annotations(frame, detections)
    frame = collision_det.draw_collision_warnings(frame, detections)
    frame = heatmap.render_heatmap_on_frame(frame)
    
    cv2.imshow("Smart Traffic", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Performance Considerations

### Memory Usage
- **Trajectory History**: ~1KB per vehicle per 10 frames
- **Heatmap Grid**: ~1MB for 1280x720 @ 32px grid
- **Collision Pairs**: O(n²) where n = vehicle count

### Speed Optimization
If processing is slow:
1. Reduce collision detection pairs: Skip distant vehicles
2. Decrease heatmap grid resolution
3. Skip incident detection on every frame (sample every 5th)
4. Disable trajectory tracking for off-screen vehicles

### Accuracy Tips
- Use high-resolution input (1080p+) for better detection
- Calibrate speed estimator for accurate m/s conversion
- Use slower prediction horizon for stable forecasts
- Balance collision sensitivity vs false positives

---

## Advanced Customization

### Custom Collision Risk Calculation
```python
class CustomCollisionDetector(CollisionDetector):
    def _calculate_collision_risk(self, pos1, vel1, pos2, vel2, box1, box2):
        # Your own algorithm
        return custom_risk_score
```

### Custom Speed Estimation
```python
class CustomSpeedEstimator(SpeedEstimator):
    def _calculate_speed(self, trajectory):
        # Use Kalman filter or other method
        return custom_speed_dict
```

### Custom Incident Detection
```python
class CustomIncidentDetector(IncidentDetector):
    def _detect_unusual_behavior(self, detections, speed_estimator):
        # Your detection logic
        self.incidents.append({...})
```

---

**Last Updated**: February 2026
**Version**: 2.0 API Reference
