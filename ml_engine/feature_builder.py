# ml_engine/feature_builder.py

from backend.services.goal_service import get_goals


def build_features(user_id):
    goals = get_goals(user_id)

    if not goals:
        return None

    total = len(goals)
    avg_streak = sum(g["current_streak"] for g in goals) / total
    best_streak = max(g["best_streak"] for g in goals)

    streak_variance = sum(
        abs(g["best_streak"] - g["current_streak"])
        for g in goals
    ) / total

    return {
        "total_goals": total,
        "avg_streak": avg_streak,
        "best_streak": best_streak,
        "streak_variance": streak_variance
    }