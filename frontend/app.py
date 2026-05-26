"""
FRONTEND: Streamlit — AI Muscle Strain & Posture Monitoring System
Connects to Flask backend at http://localhost:5000/predict
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import requests

# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Muscle Health Monitor",
    layout="wide",
    page_icon="🧍"
)

# ── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
body { background-color: #f5f7fa; }
h1 { color: #2E86C1; }
.stSlider > label { font-weight: 600; }
.metric-card {
    background: white;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ── Backend URL ────────────────────────────────────────────────
BACKEND_URL = "http://localhost:5000/predict"

# ── Header ─────────────────────────────────────────────────────
st.title("🧍 AI Muscle Strain & Posture Monitoring System")
st.markdown("### 🌿 SDG 3: Good Health & Well-being")
st.markdown("---")

# ── Layout ─────────────────────────────────────────────────────
col1, col2 = st.columns([1, 2])

# ── INPUT PANEL ────────────────────────────────────────────────
with col1:
    st.subheader("📡 Sensor Input Panel")

    st.markdown("#### 📐 IMU Sensors")
    ax = st.slider("Accelerometer X (acc_x)", -10.0, 10.0, 0.0, 0.1)
    ay = st.slider("Accelerometer Y (acc_y)", -10.0, 10.0, 0.0, 0.1)
    az = st.slider("Accelerometer Z (acc_z)", -10.0, 10.0, 9.8, 0.1)

    gx = st.slider("Gyroscope X (gyro_x)", -300.0, 300.0, 0.0, 1.0)
    gy = st.slider("Gyroscope Y (gyro_y)", -300.0, 300.0, 0.0, 1.0)
    gz = st.slider("Gyroscope Z (gyro_z)", -300.0, 300.0, 0.0, 1.0)

    st.markdown("#### 💪 EMG Sensors (0.0 – 1.0)")
    emg_biceps  = st.slider("Biceps  (emg_ch1)", 0.0, 1.0, 0.2, 0.01)
    emg_triceps = st.slider("Triceps (emg_ch2)", 0.0, 1.0, 0.2, 0.01)
    emg_back    = st.slider("Back    (emg_ch3)", 0.0, 1.0, 0.2, 0.01)
    emg_leg     = st.slider("Leg     (emg_ch4)", 0.0, 1.0, 0.2, 0.01)

    predict_btn = st.button("🔍 Analyze", use_container_width=True, type="primary")

# ── BACKEND CALL ───────────────────────────────────────────────
prediction    = None
confidence    = None
affected_areas = []
error_msg     = None

if predict_btn:
    payload = {
        "acc_x":  ax,  "acc_y":  ay,  "acc_z":  az,
        "gyro_x": gx,  "gyro_y": gy,  "gyro_z": gz,
        "emg_ch1": emg_biceps,
        "emg_ch2": emg_triceps,
        "emg_ch3": emg_back,
        "emg_ch4": emg_leg,
    }
    try:
        resp = requests.post(BACKEND_URL, json=payload, timeout=5)
        resp.raise_for_status()
        result        = resp.json()
        prediction    = result["prediction"]
        confidence    = result["confidence"]
        affected_areas = result["affected_areas"]
    except requests.exceptions.ConnectionError:
        error_msg = "❌ Cannot connect to backend. Make sure the Flask server is running on http://localhost:5000"
    except Exception as e:
        error_msg = f"❌ Error: {e}"

# ── OUTPUT PANEL ───────────────────────────────────────────────
with col2:
    st.subheader("🧠 Health Analysis Dashboard")

    # ── Connection / error status
    if error_msg:
        st.error(error_msg)
    elif prediction is None:
        st.info("👈 Adjust sensor sliders and click **Analyze** to get a prediction.")
    else:
        # ── Prediction result
        if prediction == "Normal":
            st.success(f"✅ **Healthy Condition** — No strain detected  ·  Confidence: {confidence*100:.1f}%")
        else:
            st.error(f"⚠️ **{prediction}**  ·  Confidence: {confidence*100:.1f}%")

        st.markdown("---")

        # ── 3D Body Visualisation
        st.markdown("### 🧍 3D Body Visualisation")

        fig = plt.figure(figsize=(5, 6))
        ax3d = fig.add_subplot(111, projection="3d")

        # Skeleton key points
        head  = [0,   0,   1.1]
        neck  = [0,   0,   0.9]
        spine = [ax / 40, ay / 40, 0.5]   # lean based on IMU
        hip   = [0,   0,   0.0]

        left_arm  = [-0.35, 0, 0.75]
        right_arm = [ 0.35, 0, 0.75]
        left_leg  = [-0.18, 0, -0.55]
        right_leg = [ 0.18, 0, -0.55]

        # Colors: red = strained, blue = healthy
        c_back = "red"  if "Back Strain"    in affected_areas else "#2196F3"
        c_arm  = "red"  if ("Biceps Strain" in affected_areas or
                             "Triceps Strain" in affected_areas) else "#2196F3"
        c_leg  = "red"  if "Leg Strain"     in affected_areas else "#2196F3"

        # Draw skeleton
        # Spine
        ax3d.plot(
            [head[0], neck[0], spine[0], hip[0]],
            [head[1], neck[1], spine[1], hip[1]],
            [head[2], neck[2], spine[2], hip[2]],
            color=c_back, linewidth=3, marker="o"
        )
        # Left arm
        ax3d.plot([neck[0], left_arm[0]],  [neck[1], left_arm[1]],
                  [neck[2], left_arm[2]],  color=c_arm, linewidth=2.5)
        # Right arm
        ax3d.plot([neck[0], right_arm[0]], [neck[1], right_arm[1]],
                  [neck[2], right_arm[2]], color=c_arm, linewidth=2.5)
        # Left leg
        ax3d.plot([hip[0], left_leg[0]],   [hip[1], left_leg[1]],
                  [hip[2], left_leg[2]],   color=c_leg, linewidth=2.5)
        # Right leg
        ax3d.plot([hip[0], right_leg[0]],  [hip[1], right_leg[1]],
                  [hip[2], right_leg[2]],  color=c_leg, linewidth=2.5)

        ax3d.set_xlim([-1, 1])
        ax3d.set_ylim([-1, 1])
        ax3d.set_zlim([-0.8, 1.4])
        ax3d.set_title(f"Prediction: {prediction}", fontsize=10, color="darkred" if prediction != "Normal" else "green")
        ax3d.set_xlabel("X"); ax3d.set_ylabel("Y"); ax3d.set_zlabel("Z")

        st.pyplot(fig)
        plt.close()

        st.markdown("---")

        # ── Confidence bar
        st.markdown("### 📊 Confidence Score")
        st.progress(confidence)
        st.caption(f"{confidence*100:.1f}% model confidence")

        st.markdown("---")

        # ── Recommendations
        st.markdown("### 💡 Recommendations")
        if prediction == "Normal":
            st.info("✅ Maintain healthy posture and regular exercise routines.")
        else:
            if "Back Strain" in affected_areas:
                st.warning("🔴 **Back Strain**: Maintain upright posture. Avoid prolonged sitting. Try lumbar support.")
            if "Biceps Strain" in affected_areas:
                st.warning("🔴 **Biceps Strain**: Avoid heavy lifting. Apply cold therapy. Rest the arm.")
            if "Triceps Strain" in affected_areas:
                st.warning("🔴 **Triceps Strain**: Avoid pushing motions. Apply ice pack. Consider physiotherapy.")
            if "Leg Strain" in affected_areas:
                st.warning("🔴 **Leg Strain**: Take rest. Avoid excessive walking. Elevate the leg when resting.")

# ── Footer ─────────────────────────────────────────────────────
st.markdown("---")
st.caption("🌿 AI Muscle Health Monitor · SDG 3: Good Health & Well-being · Powered by RandomForest + Flask + Streamlit")
