# ============================================================
# BACKEND: Flask API — Muscle Strain & Posture Detection
# Uses: RandomForestClassifier (model.pkl) + LabelEncoder (label_encoder.pkl)
# Features: acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z,
#           emg_ch1 (biceps), emg_ch2 (triceps), emg_ch3 (back), emg_ch4 (leg)
# ============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from Streamlit frontend

# ── Load model & label encoder ───────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "model.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(BASE_DIR, "label_encoder.pkl"), "rb") as f:
    label_encoder = pickle.load(f)

# ── Health check ─────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "message": "Muscle Health Monitor API is running ✅"})


# ── Prediction endpoint ───────────────────────────────────────
@app.route("/predict", methods=["POST"])
def predict():
    """
    Expects JSON body:
    {
        "acc_x": float,   "acc_y": float,   "acc_z": float,
        "gyro_x": float,  "gyro_y": float,  "gyro_z": float,
        "emg_ch1": float, "emg_ch2": float, "emg_ch3": float, "emg_ch4": float
    }
    Returns:
    {
        "prediction": str,      // e.g. "Normal" or "Biceps Strain, Back Strain"
        "confidence": float,    // 0.0–1.0
        "affected_areas": list  // parsed list of strained muscles
    }
    """
    try:
        data = request.get_json(force=True)

        # Build feature vector in the exact order the model was trained on
        features = np.array([[
            float(data.get("acc_x",  0.0)),
            float(data.get("acc_y",  0.0)),
            float(data.get("acc_z",  9.8)),
            float(data.get("gyro_x", 0.0)),
            float(data.get("gyro_y", 0.0)),
            float(data.get("gyro_z", 0.0)),
            float(data.get("emg_ch1", 0.0)),   # biceps
            float(data.get("emg_ch2", 0.0)),   # triceps
            float(data.get("emg_ch3", 0.0)),   # back
            float(data.get("emg_ch4", 0.0)),   # leg
        ]])

        # Predict
        pred_encoded = model.predict(features)[0]
        pred_proba   = model.predict_proba(features)[0]
        confidence   = float(np.max(pred_proba))

        # Decode label
        prediction = label_encoder.inverse_transform([pred_encoded])[0]

        # Parse affected areas for easy frontend use
        if prediction == "Normal":
            affected_areas = []
        else:
            affected_areas = [area.strip() for area in prediction.split(",")]

        return jsonify({
            "prediction":    prediction,
            "confidence":    round(confidence, 4),
            "affected_areas": affected_areas
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    print("🚀 Starting Muscle Health Monitor API on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
