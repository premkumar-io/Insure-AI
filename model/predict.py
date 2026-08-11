import os
import sys
import pickle
import traceback
import pandas as pd
import logging

logger = logging.getLogger("insure_ai.predict")

# Backward compatibility patch for pickled pipelines from older scikit-learn versions
try:
    import sklearn.compose._column_transformer
    class _RemainderColsList(list):
        def __init__(self, *args, **kwargs):
            if args:
                super().__init__(args[0])
            else:
                super().__init__()

    setattr(sklearn.compose._column_transformer, "_RemainderColsList", _RemainderColsList)
    if "sklearn.compose._column_transformer" in sys.modules:
        sys.modules["sklearn.compose._column_transformer"]._RemainderColsList = _RemainderColsList
except Exception as patch_ex:
    logger.warning(f"Could not apply _RemainderColsList patch: {patch_ex}")

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
    "/var/task/model.pkl",
    "/var/task/user/model/model.pkl"
]

_model_cache = None
MODEL_PATH = None
model_load_error = None
MODEL_VERSION = "1.0.0"
class_labels = ["Low", "Medium", "High"]

def get_model():
    global _model_cache, MODEL_PATH, model_load_error, class_labels
    if _model_cache is not None:
        return _model_cache

    for p in candidate_paths:
        if os.path.exists(p):
            MODEL_PATH = p
            break

    if MODEL_PATH:
        try:
            with open(MODEL_PATH, "rb") as f:
                _model_cache = pickle.load(f)
            if hasattr(_model_cache, "classes_"):
                class_labels = _model_cache.classes_.tolist()
            logger.info(f"Successfully loaded Random Forest model from {MODEL_PATH}")
            return _model_cache
        except Exception as ex:
            model_load_error = f"Unpickle error from {MODEL_PATH}: {type(ex).__name__}: {str(ex)}\n{traceback.format_exc()}"
            logger.error(model_load_error)
            return None
    else:
        model_load_error = f"model.pkl not found. Candidates checked: {candidate_paths}"
        logger.error(model_load_error)
        return None

# Initial attempt
model = get_model()

def predict_output(user_input: dict):
    m = get_model()
    if m is None:
        raise RuntimeError(f"ML Model is not loaded into memory. Detail: {model_load_error}")

    df = pd.DataFrame([user_input])

    # Predict the class
    predicted_class = str(m.predict(df)[0])

    # Get probabilities for all classes
    probabilities = m.predict_proba(df)[0]
    confidence = float(max(probabilities))

    # Create mapping: {class_name: probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(float(p), 4), probabilities)))

    return {
        "predicted_category": predicted_class,
        "confidence": round(confidence, 4),
        "class_probabilities": class_probs
    }