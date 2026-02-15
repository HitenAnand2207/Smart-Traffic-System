# 🏙️ Smart Traffic Analytics System - Enhanced Edition

A sophisticated AI-powered traffic management system that uses YOLOv8 detection, advanced tracking, and machine learning to provide real-time traffic insights, collision prevention, and adaptive signal control.

---

## 🚀 New Features

### 1. **🚨 Collision Detection & Avoidance System** (NEW)
- **Real-time Collision Risk Detection**: Predicts potential collisions between vehicles using trajectory analysis
- **Risk Scoring**: Calculates collision risk scores (0-1) based on:
  - Distance between vehicles
  - Relative velocities
  - Approaching factors
- **Visual Warnings**: Displays collision alerts with risk levels on video feed
- **Multi-vehicle Analysis**: Monitors all tracked vehicles simultaneously

**Key Benefits:**
- Prevent accidents before they happen
- Alert drivers of dangerous proximity
- Improve traffic safety metrics

---

### 2. **📈 Traffic Flow Prediction** (NEW)
- **Time-Series Forecasting**: Predicts future traffic congestion and vehicle counts
- **Exponential Smoothing**: Uses advanced smoothing algorithms for accurate predictions
- **Trend Analysis**: Detects traffic flow patterns and trends
- **Anomaly Detection**: Identifies unusual traffic events (sudden congestion, accidents)
- **Forecast Horizon**: Predicts up to 30 frames (~1 second) into the future

**Prediction Metrics:**
- Vehicle count forecasts
- Congestion level predictions
- Average speed projections
- Risk level assessments

---

### 3. **🗺️ Heatmap Visualization** (NEW)
- **Traffic Density Heatmaps**: Shows congestion hotspots in real-time
- **Temporal Accumulation**: Displays high-traffic zones over time
- **Grid-Based Analysis**: Divides frame into cells for detailed spatial analysis
- **Regional Congestion Index**: Calculates congestion for 9 frame regions
- **Hotspot Detection**: Identifies and ranks congested areas

**Features:**
- Interactive heatmap overlay on video
- Color-coded density visualization
- Zone-specific analytics
- Historical traffic pattern tracking

---

### 4. **⚡ Speed & Direction Estimation** (NEW)
- **Pixel-to-Meter Calibration**: Converts pixel distances to real-world speeds
- **Multi-Frame Velocity Tracking**: Calculates speed from trajectory history
- **Direction Vector Analysis**: Determines vehicle heading/direction
- **Speed Stability Index**: Measures driving consistency
- **Vector Visualization**: Draws speed vectors on detections

**Speed Analysis:**
- Individual vehicle speeds (m/s and pixels/frame)
- Fleet average speeds
- Speed distribution histograms
- Acceleration/deceleration detection

---

### 5. **🚨 Incident Detection System** (NEW)
- **Stalled Vehicle Detection**: Identifies stopped vehicles on roads
- **Erratic Driving Detection**: Detects unusual acceleration/deceleration patterns
- **Accident Detection**: Identifies overlapping vehicles and collisions
- **Incident Logging**: Maintains incident history with severity levels
- **Incident Classification**: Categorizes incidents by type and severity

**Incident Types:**
- `stalled_vehicle`: Vehicles stopped in traffic
- `erratic_driving`: Unusual movement patterns
- `potential_accident`: Overlapping vehicles
- `sudden_speed_change`: Rapid speed variations

---

### 6. **📊 Enhanced Analytics Dashboard** (NEW)
Multiple specialized view modes:

- **Live Dashboard**: Real-time metrics and multi-tab analysis
- **Collision Alerts**: Dedicated collision monitoring and statistics
- **Traffic Prediction**: Forecast and anomaly detection
- **Speed Analysis**: Detailed speed statistics and histograms
- **Incident Report**: Comprehensive incident logging and history
- **Heatmap Analytics**: Spatial congestion analysis
- **Statistics Dashboard**: Historical trends and performance metrics

**Dashboard Components:**
- Real-time metric cards with delta indicators
- Multi-tab analysis interface
- Interactive Plotly charts
- Tabular data displays

---

### 7. **🎯 Advanced Signal Recommendation System** (ENHANCED)
Improved traffic light timing recommendations based on:
- Current vehicle density
- Historical averages
- Traffic trends
- Congestion forecasts
- Violation history

**Recommendation Levels:**
- 🔴 High Traffic: Extend Green by 20s
- 🟡 Moderate Traffic: Extend Green by 10s
- 🟢 Light Traffic: Maintain Normal Timing
- 🟢 Very Light: Reduce Green by 5s

---

### 8. **📍 Trajectory Tracking** (ENHANCED)
- Maintains detailed trajectory history for each vehicle
- Supports trajectory visualization with fading effects
- Tracks up to 120 frames of history per vehicle
- Enables retrospective analysis of vehicle paths

---

## 🛠️ Technology Stack

**Machine Learning:**
- YOLOv8 (Detection)
- ByteTrack (Multi-object tracking)
- OpenCV (Image processing)
- NumPy/SciPy (Data processing)

**Backend:**
- Python 3.x
- Streamlit (UI)
- Plotly (Interactive visualizations)
- Pandas (Data handling)

**New Libraries:**
- `scipy`: Advanced mathematical operations
- `scikit-learn`: Machine learning utilities
- `matplotlib`: Additional visualization support
- `altair`: Alternative charting library

---

## 📊 System Architecture

```
Input Video/Webcam
      ↓
[YOLOv8 Detector] → Detections
      ↓
[ByteTrack Tracker] → Tracked Objects
      ↓ (Parallel Processing)
├─→ [Speed Estimator]
├─→ [Collision Detector]
├─→ [Incident Detector]
├─→ [Heatmap Generator]
├─→ [Traffic Predictor]
└─→ [Analytics Module]
      ↓
[Streamlit Dashboard] → Visualization & Recommendations
```

---

## 🎮 Controls & Settings

### Sidebar Options

**Input Source:**
- Upload Video: Process pre-recorded traffic video
- Webcam (Demo): Real-time webcam streaming

**Analysis Modes:**
- Live Dashboard: Real-time comprehensive analysis
- Collision Alerts: Focus on collision prevention
- Traffic Prediction: Future traffic forecasting
- Speed Analysis: Vehicle speed statistics
- Incident Report: Incident tracking and analysis
- Heatmap Analytics: Spatial congestion analysis
- Statistics Dashboard: Historical performance metrics

**System Settings:**
- **Enable Heatmap Overlay**: Overlay traffic density heatmap
- **Show Speed Vectors**: Display velocity vectors on detections
- **Show Vehicle Trajectories**: Draw trajectory trails
- **Collision Detection Sensitivity**: Adjust collision alert threshold (0.3-1.0)

---

## 📈 Metrics & KPIs

### Real-Time Metrics
- **Risk Index**: Safety risk score (0-100)
- **Active Vehicles**: Current vehicle count
- **Average Speed**: Fleet average speed (m/s)
- **Collision Alerts**: Active collision warnings

### Analytics
- **Total Vehicles**: Cumulative vehicle detections
- **Peak Congestion**: Maximum vehicles in frame
- **Violations**: Traffic rule violations
- **Incidents**: Detected traffic incidents
- **CO2 Emissions**: Estimated emissions (g/min)
- **Vehicle Distribution**: Breakdown by vehicle type

### Predictions
- **Congestion Forecast**: Future congestion levels
- **Risk Level**: Predicted safety risk
- **Vehicle Count Forecast**: Predicted vehicle counts

---

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Model settings
CONFIDENCE_THRESHOLD = 0.3
IOU_THRESHOLD = 0.45
VEHICLE_CLASSES = [2, 3, 5, 7, 1]  # COCO class IDs

# Emission factors (g CO2/min)
EMISSION_FACTORS = {
    "car": 120.0,
    "bus": 450.0,
    "truck": 500.0,
    "motorcycle": 60.0,
    "bicycle": 0.0
}

# Stop line position (0-1, normalized)
STOP_LINE_Y = 0.7
```

---

## 📦 Installation

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download YOLOv8 model (automatic on first run)
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

---

## 🚀 Usage

```bash
# Start Streamlit dashboard
streamlit run app.py

# Then:
# 1. Select input source (Upload or Webcam)
# 2. Choose analysis mode
# 3. Configure system settings
# 4. Upload video or start webcam
# 5. View real-time analysis and recommendations
```

---

## 📊 Output & Analytics

### Real-Time Outputs
- Annotated video with detections and tracking
- Collision warning overlays
- Speed vector visualization
- Trajectory trails
- Heatmap overlays

### Data Exports
- Session statistics and metrics
- Violation logs
- Incident reports
- Vehicle trajectories
- Performance analytics

---

## 🔍 Advanced Features

### Collision Detection Algorithm
```
For each vehicle pair:
1. Calculate distance between centroids
2. Estimate velocity vectors from trajectory
3. Check if vehicles are approaching
4. Calculate relative velocity
5. Compute collision risk score
6. Alert if risk > threshold
```

### Traffic Prediction Algorithm
```
1. Collect historical metrics (vehicle count, speed, congestion)
2. Calculate exponential smoothing with alpha
3. Estimate trend component
4. Generate forecast for N frames ahead
5. Detect anomalies using z-score analysis
```

### Speed Estimation Algorithm
```
1. Track vehicle positions across frames
2. Calculate distances between consecutive frames
3. Apply smoothing filter
4. Estimate velocity magnitude and direction
5. Convert pixels/frame to m/s using calibration factor
6. Compute stability metric from variance
```

---

## 🎯 Use Cases

1. **Traffic Management**: Optimize signal timing and traffic flow
2. **Safety Monitoring**: Detect collisions and dangerous driving
3. **Incident Response**: Quick identification and logging of incidents
4. **Urban Planning**: Analyze traffic patterns and congestion hotspots
5. **Emission Reduction**: Monitor and reduce traffic-related emissions
6. **Predictive Maintenance**: Forecast traffic issues before they occur
7. **Performance Analytics**: Track system effectiveness over time

---

## 📝 API Reference

### Key Classes

**CollisionDetector**
```python
detector = CollisionDetector(frame_width=1280, frame_height=720)
detector.update(detections, frame_time)
alerts = detector.get_alerts()
frame = detector.draw_collision_warnings(frame, detections)
```

**TrafficPredictor**
```python
predictor = TrafficPredictor(history_length=60, prediction_horizon=30)
predictor.update(vehicle_count, avg_speed, congestion, timestamp)
forecast = predictor.get_congestion_forecast()
anomalies = predictor.get_anomaly_detection()
```

**SpeedEstimator**
```python
estimator = SpeedEstimator(fps=30, pixels_per_meter=50.0)
estimator.update(detections)
speeds = estimator.get_all_speeds()
avg_speed = estimator.get_average_speed()
estimator.calibrate_pixels_to_meters(1000, 50)  # 1000 pixels = 50 meters
```

**IncidentDetector**
```python
detector = IncidentDetector()
detector.update(detections, speed_estimator)
incidents = detector.get_incidents()
summary = detector.get_incident_summary()
history = detector.get_incident_history()
```

**HeatmapGenerator**
```python
generator = HeatmapGenerator(frame_width=1280, frame_height=720, grid_size=32)
generator.update(detections)
frame = generator.render_heatmap_on_frame(frame, use_temporal=False)
hotspots = generator.get_hotspots(threshold=0.5)
regions = generator.get_congestion_index_by_region()
```

---

## 🐛 Troubleshooting

**Issue: Slow performance**
- Solution: Reduce video resolution, disable heatmap overlay, lower FPS

**Issue: Collision alerts too sensitive**
- Solution: Increase collision_sensitivity slider in sidebar (0.3-1.0)

**Issue: Speed estimates inaccurate**
- Solution: Calibrate pixels_per_meter using known distance

**Issue: Memory issues with long videos**
- Solution: Process in chunks, reduce trajectory history length

---

## 📜 License

This project uses YOLOv8 (GPL-3.0) and other open-source libraries.

---

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Lane detection and lane-specific analysis
- Weather impact analysis
- License plate detection and tracking
- Vehicle type classification refinement
- Deep learning-based speed estimation
- Multi-camera fusion support

---

## 📞 Support

For issues and feature requests, please create an issue in the repository.

---

**Last Updated**: February 2026
**Version**: 2.0 (Enhanced Edition)
