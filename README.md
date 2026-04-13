# Smart Traffic Analytics System

An AI-powered traffic monitoring and decision-support dashboard built with YOLOv8, OpenCV, Supervision ByteTrack, and Streamlit.

The system analyzes traffic video streams in near real time and provides:
- vehicle detection and tracking
- safety and risk signals
- collision and incident alerts
- traffic trend forecasting
- congestion heatmaps
- speed analytics
- advisory signal recommendations

## Highlights

- Real-time detection and tracking for cars, buses, trucks, motorcycles, and bicycles
- Collision risk scoring between tracked vehicles
- Incident detection (stalled vehicles, erratic behavior, potential accidents)
- Traffic forecasting with anomaly detection and confidence scoring
- Heatmap-based congestion hotspot analysis
- Emission estimation and explainable risk breakdown
- Decision Lab with near-miss summary and signal what-if simulation
- Session export tools for CSV/JSON reporting and dashboard reset
- Performance profiles for local and hosted Streamlit environments

## Dashboard Modes

The sidebar mode selector supports:
- Live Dashboard
- Collision Alerts
- Traffic Prediction
- Speed Analysis
- Incident Report
- Heatmap Analytics
- Statistics Dashboard

## Tech Stack

- Python 3.11
- Streamlit
- Ultralytics YOLOv8
- OpenCV
- Supervision (ByteTrack)
- NumPy, Pandas, SciPy, scikit-learn
- Plotly, Matplotlib, Altair

## Project Structure

```text
smart-traffic/
|- app.py
|- config.py
|- requirements.txt
|- runtime.txt
|- models/
|  |- yolov8n.pt
|- src/
|  |- detector.py
|  |- tracker.py
|  |- analytics.py
|  |- collision_detector.py
|  |- speed_estimator.py
|  |- incident_detector.py
|  |- traffic_predictor.py
|  |- heatmap_generator.py
|- data/
|  |- logs/
|  |- videos/
|- reports/
|- report_assets/
```

## Quick Start

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the dashboard

```bash
streamlit run app.py
```

Open the app in your browser (typically http://localhost:8501).

## Input Options

- Upload Video (mp4, avi, mov)
- Webcam (Demo)

Recommended for reproducible analysis: use uploaded video files.

## Key Features Explained

### 1) Detection and Tracking

- YOLOv8 detects supported vehicle classes
- ByteTrack assigns persistent IDs across frames
- Optional trajectory rendering visualizes movement paths

### 2) Risk and Safety

- Composite risk index (0 to 100)
- Stop-line crossing violation logging
- Risk decomposition by component in Decision Lab

### 3) Collision Alerts

- Pairwise collision-risk scoring from trajectory and relative motion
- On-frame warning overlays for high-risk pairs
- Near-miss summary with TTC-style approximation

### 4) Incident Detection

- Flags stalled vehicles, sudden speed changes, and potential accident patterns
- Reports severity-level incidents in dashboard alerts

### 5) Traffic Forecasting

- Short-horizon prediction from rolling history
- Congestion trend status and anomaly flags
- Forecast confidence score with explanations

### 6) Speed Analytics

- Per-vehicle speed estimation from tracked trajectories
- Average speed and histogram-based distribution
- Optional speed vectors overlaid on frames

### 7) Heatmap Analytics

- Density accumulation on a grid
- Real-time hotspots and region-level congestion indicators

### 8) Signal Recommendation (Advisory)

- Rule-based recommendations based on active vs average traffic levels
- Decision Lab what-if simulator for green-time strategy comparison

## Performance Tuning

Sidebar controls include:
- Performance Profile: Auto, Cloud Optimized, Balanced, High Accuracy
- Cloud Lite Mode: disables expensive overlays for better hosted FPS

Suggested defaults:
- Local machine: Balanced or High Accuracy
- Hosted deployment: Cloud Optimized + Cloud Lite Mode

## Configuration

Edit config values in config.py, including:
- model path and detection thresholds
- vehicle class IDs
- emission factors
- stop-line location
- dashboard title and log directory

## Troubleshooting

### Model loading issues
- Ensure requirements are installed and internet is available on first model pull.
- Verify model file exists at models/yolov8n.pt.

### Slow performance
- Switch to Cloud Optimized profile.
- Enable Cloud Lite Mode.
- Disable heatmap, trajectory, or speed vectors.
- Use lower-resolution input video.

### No detections
- Check video quality and lighting.
- Lower confidence threshold in config.py.

### Streamlit command not found
- Activate your virtual environment before running the app.

## Additional Documentation

For deeper details, see:
- QUICKSTART.md
- FEATURES.md
- ARCHITECTURE.md
- API_REFERENCE.md
- FILE_REFERENCE.md
- ENHANCEMENT_SUMMARY.md

## Notes

- Current recommendations are advisory and should not be treated as direct traffic-control commands.
- The system is intended for analytics, experimentation, and decision support workflows.
