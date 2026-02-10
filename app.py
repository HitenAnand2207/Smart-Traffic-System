import streamlit as st
import cv2
import tempfile
import numpy as np
import pandas as pd
import time
from PIL import Image
import supervision as sv
from src.detector import TrafficDetector
from src.tracker import TrafficTracker
from src.analytics import TrafficAnalytics
import config

# Page Config
st.set_page_config(page_title=config.DASHBOARD_TITLE, layout="wide")

# Initialize components
@st.cache_resource
def load_models():
    return TrafficDetector(), TrafficTracker(), TrafficAnalytics()

detector, tracker, analytics = load_models()

# Sidebar
st.sidebar.title("🚦 System Controls")
app_mode = st.sidebar.selectbox("Choose Mode", ["Traffic Analyst", "Control Room"])
source_option = st.sidebar.radio("Input Source", ["Upload Video", "Webcam (Demo)"])

uploaded_file = None
if source_option == "Upload Video":
    uploaded_file = st.sidebar.file_uploader("Upload Traffic Video", type=["mp4", "avi", "mov"])

# Main Dashboard
st.title(f"🏙️ {config.DASHBOARD_TITLE}")

# Layout Columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Live Analysis Feed")
    frame_placeholder = st.empty()

with col2:
    st.subheader("Real-Time Analytics")
    risk_metric = st.metric("Safety Risk Index", "0.00", delta_color="inverse")
    pollution_metric = st.metric("CO2 Emissions (est. g/min)", "0.0")
    signal_rec = st.info("Signal Recommendation: System Initializing...")
    
    # Violation Table
    st.write("### 🚨 Violation Log")
    violation_placeholder = st.empty()

# Stats Row
st.divider()
chart_col1, chart_col2 = st.columns(2)

# Global state for charts
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Time", "Risk", "Pollution"])

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Create SV components for helper drawing
    label_annotator = sv.LabelAnnotator()
    mask_annotator = sv.MaskAnnotator()
    
    start_time = time.time()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 1. Detection
        results = detector.detect(frame)
        detections = sv.Detections.from_ultralytics(results)
        
        # Add class_name to detections for labeling
        detections.data['class_name'] = np.array([detector.get_class_name(c) for c in detections.class_id])
        
        # 2. Tracking
        detections = tracker.update(detections)
        
        # 3. Analytics
        if detections.tracker_id is not None:
             analytics.update_analytics(detections)
        
        # 4. Visualization
        annotated_frame = tracker.annotate_frame(frame, detections)
        
        # Resize for dashboard
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(annotated_frame, channels="RGB", use_container_width=True)
        
        # Update Metrics
        risk_score = analytics.calculate_risk_index()
        emissions = analytics.estimate_emissions()
        
        risk_metric.metric("Safety Risk Index", f"{risk_score:.2f}", 
                           delta=f"{risk_score - 20:.1f}" if risk_score > 20 else "Low")
        pollution_metric.metric("CO2 Emissions (est. g/min)", f"{emissions:.1f}")
        signal_rec.info(f"💡 Recommendation: {analytics.get_signal_recommendation()}")
        
        # Update Violation Log
        if analytics.violation_logs:
            df_v = pd.DataFrame(analytics.violation_logs).tail(5)
            violation_placeholder.table(df_v)
        
        # Update Chart History
        new_row = {"Time": time.time() - start_time, "Risk": risk_score, "Pollution": emissions}
        st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_row])], ignore_index=True)
        
        # Display Charts in col
        with chart_col1:
             st.line_chart(st.session_state.history.set_index("Time")["Risk"], height=200)
        with chart_col2:
             st.bar_chart(pd.Series(analytics.total_counts), height=200)

        # Control speed for demo
        # time.sleep(0.01)

    cap.release()

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    process_video(tfile.name)
elif source_option == "Webcam (Demo)":
    st.warning("Webcam mode is active. Please ensure camera access.")
    process_video(0)
else:
    st.info("Please upload a video file or select Webcam to start analysis.")
