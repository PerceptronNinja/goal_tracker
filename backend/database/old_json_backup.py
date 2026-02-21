import json
import os
from datetime import datetime, timedelta

FILE = "goals.json"


# ----------------------------
# Database Initialization
# ----------------------------
def initialize_db():
    if not os.path.exists(FILE) or os.stat(FILE).st_size == 0:
        with open(FILE, "w") as f:
            json.dump([], f)


# ----------------------------
# Load Goals (Safe Version)
# ----------------------------
def load_goals():
    initialize_db()

    try:
        with open(FILE, "r") as f:
            goals = json.load(f)
    except json.JSONDecodeError:
        goals = []

    # 🔥 Backward compatibility upgrade
    for goal in goals:
        goal.setdefault("repeat_type", "daily")
        goal.setdefault("custom_days", None)
        goal.setdefault("last_completed_date", None)
        goal.setdefault("current_streak", 0)
        goal.setdefault("best_streak", 0)
        goal.setdefault("history", [])

    return goals


# ----------------------------
# Save Goals
# ----------------------------
def save_goals(goals):
    with open(FILE, "w") as f:
        json.dump(goals, f, indent=4)


# ----------------------------
# Add Goal (New Schema)
# ----------------------------
def add_goal(title, repeat_type, reminder_time, custom_days=None):
    goals = load_goals()

    goal = {
        "title": title,
        "repeat_type": repeat_type,
        "completed": False,
        "reminder_time": reminder_time,
        "custom_days": custom_days,
        "last_completed_date": None,
        "current_streak": 0,
        "best_streak": 0,
        "history": []
    }

    goals.append(goal)
    save_goals(goals)


# ----------------------------
# Mark Completed (With Streak)
# ----------------------------
def mark_completed(index):
    goals = load_goals()

    if 0 <= index < len(goals):
        today = datetime.now().date()
        goal = goals[index]

        last_date_str = goal.get("last_completed_date")
        last_date = None
        if last_date_str:
            last_date = datetime.strptime(
                last_date_str, "%Y-%m-%d"
            ).date()

        # 🔥 Streak Logic
        if last_date == today - timedelta(days=1):
            goal["current_streak"] += 1
        elif last_date == today:
            return True  # Already completed today
        else:
            goal["current_streak"] = 1

        # Update best streak
        if goal["current_streak"] > goal["best_streak"]:
            goal["best_streak"] = goal["current_streak"]

        goal["completed"] = True
        goal["last_completed_date"] = today.strftime("%Y-%m-%d")
        goal["history"].append(today.strftime("%Y-%m-%d"))

        save_goals(goals)
        return True

    return False


# ----------------------------
# Delete Goal
# ----------------------------
def delete_goal(index):
    goals = load_goals()

    if 0 <= index < len(goals):
        goals.pop(index)
        save_goals(goals)
        return True

    return False