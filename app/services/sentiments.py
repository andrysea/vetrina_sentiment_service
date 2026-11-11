
from pathlib import Path
import pickle

MODEL_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "models"
    / "sentiment_analysis_model.pkl"
)


def load_model():
    with MODEL_PATH.open("rb") as file:
        model = pickle.load(file)

    return model


def predict_sentiment(model, review: str) -> dict:
    prediction = model.predict([review])[0]

    result = {
        "sentiment": str(prediction)
    }

    if hasattr(model, "predict_proba") and hasattr(model, "classes_"):
        probabilities = model.predict_proba([review])[0]
        class_index = list(model.classes_).index(prediction)

        result["confidence"] = float(probabilities[class_index])

    return result
