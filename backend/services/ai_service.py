# backend/services/ai_service.py

from backend.services.analytics_service import calculate_metrics


def generate_insight(user_id):
    metrics = calculate_metrics(user_id)

    performance_score = (
        metrics["avg_streak"] * 0.6 +
        metrics["total"] * 0.4
    )

    if performance_score < 5:
        return "Start with smaller consistent goals."
    elif performance_score < 15:
        return "Good progress. Improve consistency."
    else:
        return "Excellent discipline. Increase difficulty."