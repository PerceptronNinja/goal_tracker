# ml_engine/streak_prediction.py

import numpy as np
from ml_engine.model_utils import load_model
from ml_engine.feature_builder import build_features


MODEL_PATH = "ml_engine/streak_model.pkl"


def predict_streak_break(user_id):

    features = build_features(user_id)

    if not features:
        return None

    model = load_model(MODEL_PATH)

    X = np.array([[
        features["avg_streak"],
        features["best_streak"],
        features["total_goals"],
        features["streak_variance"]
    ]])

    probability = model.predict_proba(X)[0][1]

    return round(probability * 100, 2)