import os
import pickle
import pandas as pd
import logging

logger = logging.getLogger("insure_ai.predict")

# Robust candidate path resolution for local dev & Vercel serverless environments
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(MODEL_DIR)

candidate_paths = [
    os.path.join(MODEL_DIR, "model.pkl"),
    os.path.join(PROJECT_ROOT, "model", "model.pkl"),
    os.path.join(PROJECT_ROOT, "api", "model.pkl"),
    os.path.join(PROJECT_ROOT, "model.pkl"),
    os.path.join(os.getcwd(), "model", "model.pkl"),
    os.path.join(os.getcwd(), "api", "model.pkl"),
    os.path.join(os.getcwd(), "model.pkl"),
    "/var/task/model/model.pkl",
    "/var/task/api/model.pkl",
    "/var/task/model.pkl"
]

MODEL_PATH = None
for p in candidate_paths:
    if os.path.exists(p):
        MODEL_PATH = p
        break

model = None
MODEL_VERSION = "1.0.0"
class_labels = ["Low", "Medium", "High"]
model_load_error = None

if MODEL_PATH:
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        if hasattr(model, "classes_"):
            class_labels = model.classes_.tolist()
        logger.info(f"Loaded Random Forest model from {MODEL_PATH}")
    except Exception as ex:
        model_load_error = f"Unpickle error from {MODEL_PATH}: {type(ex).__name__}: {str(ex)}"
        logger.error(model_load_error)
else:
    model_load_error = f"model.pkl not found in candidates: {candidate_paths}"
    logger.error(model_load_error)

def predict_output(user_input: dict):
    if model is None:
        raise RuntimeError(f"ML Model is not loaded into memory. Detail: {model_load_error}")

    df = pd.DataFrame([user_input])

    # Predict the class
    predicted_class = str(model.predict(df)[0])

    # Get probabilities for all classes
    probabilities = model.predict_proba(df)[0]
    confidence = float(max(probabilities))

    # Create mapping: {class_name: probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(float(p), 4), probabilities)))

    return {
        "predicted_category": predicted_class,
        "confidence": round(confidence, 4),
        "class_probabilities": class_probs
    }