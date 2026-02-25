# ml_engine/train_model.py

import numpy as np
from sklearn.linear_model import LogisticRegression
from ml_engine.model_utils import save_model


def train_streak_model():

    # Synthetic training data
    X = np.array([
        [1, 2, 1, 0.5],
        [3, 5, 5, 0.2],
        [0, 1, 1, 0.8],
        [6, 8, 10, 0.1],
        [2, 3, 4, 0.6],
    ])

    y = np.array([1, 0, 1, 0, 1])  # 1 = streak break

    model = LogisticRegression()
    model.fit(X, y)

    save_model(model, "ml_engine/streak_model.pkl")


if __name__ == "__main__":
    train_streak_model()