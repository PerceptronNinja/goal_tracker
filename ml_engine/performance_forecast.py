# ml_engine/performance_forecast.py

import numpy as np
from sklearn.linear_model import LinearRegression
from backend.services.goal_service import get_goals


def forecast_performance(user_id):
    goals = get_goals(user_id)

    if not goals:
        return None

    streaks = [g["current_streak"] for g in goals]

    X = np.arange(len(streaks)).reshape(-1, 1)
    y = np.array(streaks)

    model = LinearRegression()
    model.fit(X, y)

    future_day = np.array([[len(streaks) + 7]])
    prediction = model.predict(future_day)[0]

    return round(prediction, 2)