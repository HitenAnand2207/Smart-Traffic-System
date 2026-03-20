# 🚀 Quick Start Guide - Smart Traffic System

## Installation (5 minutes)

### Step 1: Clone/Setup Project
```bash
cd smart-traffic
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

The system will automatically download the YOLOv8 nano model (~37MB) on first run.

---

## Running the System

### Basic Usage
```bash
streamlit run app.py
```

This opens the dashboard at `http://localhost:8501`

### With Video File
1. Start the app: `streamlit run app.py`
2. In sidebar: Select "Upload Video"
3. Upload a traffic video (MP4, AVI, or MOV)
4. Choose analysis mode and settings
5. Click to process

---

## 🎮 Dashboard Controls

### Main Sidebar
| Control | Options | Default |
|---------|---------|---------|
| **Mode** | 7 different analysis views | Live Dashboard |
| **Input** | Upload Video / Webcam | Upload Video |
| **Heatmap** | Enable/Disable | ON |
| **Speed Arrows** | Show/Hide vectors | ON |
| **Trajectories** | Show/Hide trails | ON |
| **Sensitivity** | Collision threshold | 0.6 |
| **Performance Profile** | Auto / Cloud Optimized / Balanced / High Accuracy | Auto |
| **Cloud Lite Mode** | ON / OFF | ON (hosted) |

If hosted on Streamlit Cloud, set **Performance Profile** to **Cloud Optimized** for smoother FPS.
For best hosted stability, keep **Cloud Lite Mode** enabled.

---

## 📊 Understanding the Dashboard

### Real-Time Metrics (Top Row)
- **🔴 Risk Index**: Safety score (0-100). Higher = more dangerous
- **🚗 Active Vehicles**: How many vehicles are currently detected
- **⚡ Avg Speed**: Fleet average speed in meters/second
- **⚠️ Collision Alerts**: Number of high-risk collision warnings
- **🎞️ Processing FPS**: Real-time processing speed (with display FPS in delta)

### 5 Analysis Tabs

#### 📊 Real-Time Tab
- Current metrics snapshot
- Signal recommendations (🔴🟡🟢)
- Congestion forecast
- Emissions estimate

#### ⚠️ Alerts Tab
- Active collision risks with vehicle IDs
- Current incidents and descriptions
- Severity levels for each alert

#### 🗺️ Spatial Tab
- High-density traffic hotspots
- Regional congestion breakdown
- 9-zone congestion grid

#### 📈 Trends Tab
- Congestion forecast graph
- Anomaly detection results
- Traffic pattern analysis

#### 🚗 Vehicles Tab
- Vehicle type distribution (pie chart)
- Speed distribution histogram
- Fleet composition analysis

---

## 📈 Key Features Explained

### 1. Collision Detection
```
What it does:
- Tracks vehicle positions frame-by-frame
- Predicts if vehicles are on collision course
- Shows red circles and warning lines on video
- Reports risk score (0-1) for each pair

How to use:
- Adjust sensitivity slider (0.3 = very sensitive, 1.0 = conservative)
- Red circles appear when collision risk is high
- Check ⚠️ Alerts tab for details
```

### 2. Traffic Prediction
```
What it does:
- Analyzes recent traffic patterns
- Predicts congestion 30 frames (~1 second) ahead
- Detects unusual traffic events

How to use:
- Check 📈 Trends tab for forecast graph
- Look for "Anomaly" warnings
- Use predictions for signal timing
```

### 3. Heatmap Visualization
```
What it does:
- Shows traffic density as colored overlay
- Red = high congestion, Blue = light traffic
- Identifies hotspots

How to use:
- Enable in sidebar settings
- Red areas are problem zones
- Use for urban planning
```

### 4. Speed Analysis
```
What it does:
- Shows speed vector arrows on vehicles
- Calculates average fleet speed
- Generates speed distribution

How to use:
- Green arrows show direction and speed
- Longer arrows = faster vehicles
- Check 🚗 Vehicles tab for histogram
```

### 5. Incident Detection
```
What it does:
- Detects stalled vehicles
- Finds erratic driving patterns
- Identifies potential accidents

How to use:
- Check ⚠️ Alerts tab
- Severity levels: Low/Medium/High
- Use for incident response
```

---

## 🎯 Example Workflows

### Workflow 1: Optimize Traffic Light Timing
1. Upload typical rush-hour video
2. Select "Live Dashboard" mode
3. Monitor "Signal Recommendation" metric
4. Follow color-coded suggestions (🔴🟡🟢)
5. Adjust signal timing accordingly

### Workflow 2: Accident Prevention
1. Select "Collision Alerts" mode
2. Lower sensitivity slider to 0.4
3. Monitor ⚠️ Alerts tab continuously
4. Watch for red circles on video
5. Identify high-risk zones

### Workflow 3: Congestion Analysis
1. Select "Heatmap Analytics" mode
2. Enable heatmap overlay
3. Watch traffic hotspots develop
4. Check 🗺️ Spatial tab for details
5. Identify recurring problem areas

### Workflow 4: Performance Report
1. Process entire day's traffic videos
2. Select "Statistics Dashboard" mode
3. Review summary metrics
4. Export visualization screenshots
5. Generate report

---

## 📊 Interpreting Metrics

### Risk Index Scale
```
0-20:   ✅ LOW RISK (green)
20-50:  🟡 MODERATE RISK (yellow)
50-75:  🟠 HIGH RISK (orange)
75-100: 🔴 CRITICAL RISK (red)
```

### Congestion Levels
```
🟢 Low Traffic      → <5 vehicles
🟡 Moderate         → 5-15 vehicles
🔴 Heavy            → >15 vehicles
```

### Collision Risk Score
```
0.0-0.3: ✅ Safe
0.3-0.6: 🟡 Watch
0.6-0.8: 🟠 Caution
0.8-1.0: 🔴 High Risk
```

---

## 🔧 Customization

### Adjust Collision Sensitivity
- **Low (0.3)**: Very sensitive, detects minor risks
- **High (1.0)**: Conservative, only critical alerts
- **Recommended**: 0.6 for balanced detection

### Change Heatmap Grid Size
Edit `src/heatmap_generator.py`:
```python
generator = HeatmapGenerator(grid_size=32)  # Larger = coarser grid
```

### Calibrate Speed to Real-World Units
1. Find a known distance on your camera (e.g., road marking)
2. Measure pixels between points
3. In sidebar settings, use: `estimator.calibrate_pixels_to_meters(pixels, meters)`

---

## 🐛 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Laggy playback | Enable "Show Speed Vectors" OFF |
| Collision alerts too many | Increase sensitivity slider to 0.8 |
| App crashes with large video | Reduce resolution, process in chunks |
| YOLOv8 model not loading | Run: `pip install --upgrade ultralytics` |
| Streamlit not found | Ensure `.venv` is activated |

---

## 📁 Project Structure

```
smart-traffic/
├── app.py                    # Main Streamlit app
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── FEATURES.md              # Feature documentation
├── QUICKSTART.md            # This file
│
├── src/
│   ├── detector.py           # YOLOv8 detection
│   ├── tracker.py            # ByteTrack tracking
│   ├── analytics.py          # Traffic analytics (ENHANCED)
│   ├── collision_detector.py # Collision detection (NEW)
│   ├── traffic_predictor.py  # Traffic prediction (NEW)
│   ├── speed_estimator.py    # Speed estimation (NEW)
│   ├── incident_detector.py  # Incident detection (NEW)
│   └── heatmap_generator.py  # Heatmap generation (NEW)
│
├── models/
│   └── yolov8n.pt           # YOLOv8 model
│
└── data/
    ├── logs/                # Log files
    └── videos/              # Test videos
```

---

## 🚀 Performance Tips

### For Faster Processing
1. Disable heatmap overlay (`-heatmap`)
2. Disable trajectory display
3. Increase collision sensitivity (fewer alerts = less processing)
4. Use lower resolution videos (720p instead of 1080p)
5. Use **Performance Profile = Cloud Optimized**
6. Turn **Cloud Lite Mode = ON** for hosted apps

### For Better Accuracy
1. Use well-lit traffic footage
2. Ensure good camera angle (birds-eye is best)
3. Calibrate speed estimates for accuracy
4. Process videos at consistent frame rates

### GPU Acceleration (Optional)
```bash
# For NVIDIA GPU support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Then set in code:
# model.to('cuda')
```

---

## 📞 Need Help?

### Check Documentation
- [FEATURES.md](FEATURES.md) - Detailed feature documentation
- [config.py](config.py) - Configuration options

### Verify Setup
```bash
# Check Python version (requires 3.8+)
python --version

# Check virtual environment
.venv\Scripts\activate && python -m pip list

# Test imports
python -c "import cv2, ultralytics, streamlit; print('✅ All imports OK')"
```

### Debug Mode
Add to app.py:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📊 Example Use Cases

| Industry | Use Case |
|----------|----------|
| **City Planning** | Analyze peak hours, identify problem intersections |
| **Insurance** | Detect dangerous driving, validate claims |
| **Transit** | Monitor bus/truck movements, optimize routes |
| **Emergency** | Detect accidents, coordinate response |
| **Environment** | Estimate emissions, reduce pollution |
| **Retail** | Monitor parking lot traffic patterns |

---

## 🎓 Learning Resources

- **YOLOv8**: https://docs.ultralytics.com/
- **Streamlit**: https://docs.streamlit.io/
- **OpenCV**: https://docs.opencv.org/
- **Supervision**: https://supervision.roboflow.com/

---

**Version**: 2.0 Enhanced Edition | **Last Updated**: February 2026
