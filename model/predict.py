import os
import pickle
import pandas as pd

# Import the ML model
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, 'model.pkl')

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

# MLflow model version
MODEL_VERSION = '1.0.0'

# Get class labels from model
class_labels = model.classes_.tolist()  # Fixed from `model_classes_`

def predict_output(user_input: dict):
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