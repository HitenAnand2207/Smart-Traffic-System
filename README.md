# Smart Traffic Analytics System

Smart Traffic Analytics System is an AI-powered traffic monitoring and decision-support dashboard. It processes traffic video streams to detect vehicles, track movement, estimate speed, surface safety risks, summarize congestion, and generate advisory analytics for operators and planners.

## What The Project Does

The application turns a traffic video or webcam feed into a live analytics dashboard. It can:

- detect vehicles in each frame
- track vehicles across time with persistent IDs
- estimate speed and movement direction
- flag collision risks and suspicious vehicle interactions
- detect incidents such as stalled vehicles or erratic motion
- generate heatmaps for congestion hotspots
- forecast near-term traffic trends
- produce advisory signal recommendations and summary reports

## Why It Exists

This project is meant to support traffic analysis, not replace a traffic operator. The goal is to provide a practical tool for:

- observing traffic conditions in near real time
- understanding congestion patterns and bottlenecks
- identifying safety risks early
- creating data-driven summaries for review and planning
- experimenting with traffic decision support in a controlled environment

The recommendations in the dashboard are advisory only and should not be treated as direct traffic-control commands.

## Main Capabilities

- Real-time detection and tracking for cars, buses, trucks, motorcycles, and bicycles
- Collision risk scoring between nearby tracked vehicles
- Incident detection for stalled vehicles, sudden motion changes, and accident-like patterns
- Short-horizon traffic forecasting with anomaly and confidence indicators
- Congestion heatmaps and spatial hotspot analysis
- Speed analytics with distribution charts and per-vehicle estimates
- Session export tools for CSV and JSON reporting
- Performance profiles for local and hosted Streamlit deployments

## Tech Stack And Purpose

| Technology | Purpose |
| --- | --- |
| Python | Core application language and analytics logic |
| Streamlit | Web dashboard UI, controls, metrics, and reporting views |
| Ultralytics YOLOv8 | Vehicle detection in video frames |
| OpenCV | Video input, frame handling, and image processing |
| Supervision / ByteTrack | Multi-object tracking with persistent IDs |
| NumPy | Efficient numerical operations on frame and metric data |
| Pandas | Session history, tabular analytics, and report exports |
| SciPy | Supporting statistical and mathematical calculations |
| scikit-learn | Lightweight machine-learning utilities used in analytics workflows |
| Plotly | Interactive charts and dashboards |
| Matplotlib | Additional plotting support for analytics views |
| Altair | Alternative charting and visualization layer |
| python-dotenv | Environment variable loading for local configuration |
| PyYAML | Structured configuration support |

## Dashboard Modes

The sidebar mode selector includes:

- Live Dashboard
- Collision Alerts
- Traffic Prediction
- Speed Analysis
- Incident Report
- Heatmap Analytics
- Statistics Dashboard

## How It Works

1. A video or webcam stream is loaded into the dashboard.
2. YOLOv8 detects supported vehicle classes in each frame.
3. ByteTrack keeps vehicle identities consistent across frames.
4. The analytics modules calculate risk, speed, incident, prediction, and heatmap outputs.
5. Streamlit renders the live results, charts, alerts, and downloadable summaries.

## Notes

- The system is intended for analytics, experimentation, and decision support workflows.
- Results depend on video quality, camera angle, and scene complexity.
