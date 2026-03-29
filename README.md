# Surface Defect Detection System

A web-based automated defect detection system built with **FastAPI**, **OpenCV**, and **Scikit-learn** for real-time surface inspection and anomaly classification.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Image Processing | OpenCV |
| Anomaly Detection | Scikit-learn (Isolation Forest) |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |

## Features

- Upload surface images via browser UI
- Automated defect detection using edge detection & contour analysis
- Severity classification: None / Low / Medium / High
- Anomaly detection using Isolation Forest (unsupervised ML)
- Inspection history stored in SQLite with timestamp
- Auto-generated API docs at `/docs`

## Project Structure

```
defect-detection/
├── app.py              # FastAPI routes
├── detector.py         # OOP-based OpenCV pipeline
├── models/
│   └── analyzer.py     # Scikit-learn anomaly detection
├── database/
│   └── db.py           # SQLite logger
├── templates/
│   └── index.html      # Web UI
├── static/uploads/     # Uploaded images
├── requirements.txt
└── README.md
```

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start server
uvicorn app:app --reload

# 3. Open browser
# http://localhost:8000       → Web UI
# http://localhost:8000/docs  → Swagger API docs
```

## How It Works

1. User uploads an image via the web interface
2. OpenCV pipeline: Grayscale → Gaussian Blur → Canny Edge Detection → Contour Analysis
3. Features extracted: defect count, defect area ratio, intensity stats
4. Isolation Forest model flags statistical anomalies
5. Result (severity + confidence) returned and logged to SQLite
