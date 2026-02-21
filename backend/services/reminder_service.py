# backend/services/reminder_service.py

from backend.services.goal_service import get_goals
from datetime import datetime


def check_daily_reminders(user_id):
    goals = get_goals(user_id)
    now = datetime.now().strftime("%H:%M")

    alerts = []

    for goal in goals:
        if goal["repeat_type"] == "daily" and goal["reminder_time"] == now:
            alerts.append(f"Reminder: {goal['title']}")

    return alerts