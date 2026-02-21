# backend/services/analytics_service.py

from backend.services.goal_service import get_goals


def calculate_metrics(user_id):
    goals = get_goals(user_id)

    if not goals:
        return {
            "total": 0,
            "avg_streak": 0,
            "best_streak": 0
        }

    total = len(goals)
    avg_streak = sum(g["current_streak"] for g in goals) / total
    best_streak = max(g["best_streak"] for g in goals)

    return {
        "total": total,
        "avg_streak": avg_streak,
        "best_streak": best_streak
    }