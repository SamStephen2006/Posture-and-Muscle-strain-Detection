# 🧍 AI-Based Muscle Strain & Posture Monitoring System

An intelligent healthcare monitoring system designed to detect muscle strain and posture abnormalities in real time using Machine Learning, IMU sensors, and EMG sensor data. The project combines a Flask-based backend API with a Streamlit-powered frontend dashboard to provide accurate posture analysis, strain prediction, and health monitoring.

---

## 📌 Features

- Real-time posture monitoring
- Muscle strain detection and prediction
- Machine Learning–based classification
- REST API integration using Flask
- Interactive frontend dashboard using Streamlit
- EMG and IMU sensor data processing
- Confidence-based prediction results
- Lightweight and scalable architecture

---

## 🏗️ Project Architecture

```text
muscle_health/
├── backend/
│   ├── app.py                # Flask REST API
│   ├── model.pkl             # Trained RandomForest Model
│   ├── label_encoder.pkl     # Sklearn Label Encoder
│   └── requirements.txt

├── frontend/
│   ├── app.py                # Streamlit User Interface
│   └── requirements.txt

└── README.md
```

---

## ⚙️ Technologies Used

- Python
- Flask
- Streamlit
- Scikit-learn
- Machine Learning
- REST API
- IMU Sensor Data
- EMG Signal Processing

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/SamStephen2006/Posture-and-Muscle-strain-Detection.git
cd Posture-and-Muscle-strain-Detection
```

---

### 2️⃣ Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

### 3️⃣ Start the Backend Server

```bash
python app.py
```

Backend server will run at:

```text
http://localhost:5000
```

---

### 4️⃣ Install Frontend Dependencies

Open a new terminal window:

```bash
cd frontend
pip install -r requirements.txt
```

---

### 5️⃣ Launch the Frontend Application

```bash
streamlit run app.py
```

Frontend dashboard will run at:

```text
http://localhost:8501
```

---

## 🔌 API Endpoints

### Health Check

```http
GET /
```

Response:

```json
{
  "status": "ok"
}
```

---

### Predict Muscle Strain & Posture Condition

```http
POST /predict
```

### Sample Request

```json
{
  "acc_x": 0.0,
  "acc_y": 0.0,
  "acc_z": 9.8,
  "gyro_x": 0.0,
  "gyro_y": 0.0,
  "gyro_z": 0.0,
  "emg_ch1": 0.2,
  "emg_ch2": 0.2,
  "emg_ch3": 0.2,
  "emg_ch4": 0.2
}
```

### Sample Response

```json
{
  "prediction": "Biceps Strain, Back Strain",
  "confidence": 0.87,
  "affected_areas": [
    "Biceps Strain",
    "Back Strain"
  ]
}
```

---

## 🧠 Prediction Categories

| Prediction Label | Description |
|------------------|-------------|
| Normal | No strain detected |
| Biceps Strain | Stress detected in biceps muscles |
| Triceps Strain | Triceps muscle overload detected |
| Back Strain | Lumbar/back muscle stress identified |
| Leg Strain | Muscle strain detected in legs |
| Combined Strain | Multiple muscle groups affected |

---

## 🌍 Sustainable Development Goal (SDG 3)

This project supports **SDG 3 – Good Health and Well-being** by promoting intelligent healthcare monitoring and early detection of musculoskeletal strain through wearable sensing and machine learning technologies.

---

## 🔮 Future Enhancements

- Real-time wearable device integration
- Cloud-based health analytics
- Mobile application support
- Advanced deep learning models
- Real-time notification and alert system
- Patient monitoring dashboard

---

## 👨‍💻 Authors

**Samuel Stephen Chetty & Charan Bhupathi**
