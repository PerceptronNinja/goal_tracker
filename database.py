import json
import os

FILE = "goals.json"


def initialize_db():
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump([], f)


def load_goals():
    initialize_db()
    with open(FILE, "r") as f:
        return json.load(f)


def save_goals(goals):
    with open(FILE, "w") as f:
        json.dump(goals, f, indent=4)


def add_goal(title, goal_type, reminder_time):
    goals = load_goals()

    goal = {
        "title": title,
        "type": goal_type,
        "completed": False,
        "reminder_time": reminder_time
    }

    goals.append(goal)
    save_goals(goals)


def mark_completed(index):
    goals = load_goals()
    if 0 <= index < len(goals):
        goals[index]["completed"] = True
        save_goals(goals)
        return True
    return False


def delete_goal(index):
    goals = load_goals()
    if 0 <= index < len(goals):
        goals.pop(index)
        save_goals(goals)
        return True
    return False
