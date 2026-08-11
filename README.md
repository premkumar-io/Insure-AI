# 🛡️ Insure AI - Enterprise Insurance Risk Prediction Platform

Insure AI is a production-ready machine learning platform designed to assess, analyze, and classify insurance policy applicants into risk categories (**Low**, **Medium**, **High**) based on health, lifestyle, and demographic metrics.

---

## 🚀 Live Demo & Deployment

- **Vercel Web Dashboard & API**: [https://insuresai.vercel.app](https://insuresai.vercel.app)
- **Local Streamlit Dashboard**: `streamlit run frontend.py`
- **FastAPI Backend Server**: `python run.py`

---

## 🌟 Key Features

- **Random Forest Risk Classification**: High-accuracy machine learning model trained on demographic and physical health indicators.
- **Interactive Multi-Theme Dashboard**: Glassmorphic UI with live unit toggling (Meters vs. Feet & Inches), preset applicant profiles, and real-time BMI / lifestyle risk badges.
- **Dual Deployment Ready**: Fully supported for both local Streamlit UI and Vercel Serverless Functions (`api/index.py`).
- **Robust API Input Validation**: Powered by Pydantic schema validation with detailed, field-specific error messaging.
- **Full Automated Test Suite**: 14 Pytest unit and integration tests covering API endpoints, model predictions, and edge-case validations.

---

## 🛠️ Project Structure

```
Insure-AI/
├── api/
│   └── index.py            # Vercel serverless entrypoint
├── config/
│   └── city_tier.py        # Metro & Tier classification maps
├── docs/                   # Architectural & API specifications
├── model/
│   ├── model.pkl           # Trained Random Forest classifier
│   └── predict.py          # ML inference pipeline
├── schema/
│   ├── prediction_response.py # Output schema models
│   └── user_input.py       # Pydantic input validation model
├── static/
│   └── index.html          # Enterprise single-page web UI
├── tests/                  # Pytest test suite
├── app.py                  # FastAPI core application
├── frontend.py             # Streamlit web application
├── requirements.txt        # Production dependencies
├── run.py                  # Local Uvicorn server launcher
└── vercel.json             # Vercel serverless configuration
```

---

## 🧪 Running Tests Locally

```bash
pytest tests/ -v
```

---

## 📜 License

MIT License © 2026 Prem Kumar. All rights reserved.
