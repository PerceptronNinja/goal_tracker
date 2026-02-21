from plyer import notification
import schedule
import time
from datetime import datetime, timedelta
from database import load_goals, save_goals

scheduled_jobs = {}


def send_notification(title):
    notification.notify(
        title="Goal Reminder",
        message=f"Reminder: {title}",
        timeout=10
    )


def reset_daily_goal(goal, index, goals):
    repeat_type = goal.get("repeat_type", "daily")

    if repeat_type != "daily":
        return

    if not goal.get("last_completed_date"):
        return

    from datetime import datetime

    today = datetime.now().date()
    last_date = datetime.strptime(
        goal["last_completed_date"], "%Y-%m-%d"
    ).date()

    if today > last_date:
        goals[index]["completed"] = False
        goals[index]["last_completed_date"] = None
        save_goals(goals)


def schedule_goal(index, goal):
    if index in scheduled_jobs:
        return

    if not goal["reminder_time"]:
        return

    repeat_type = goal["repeat_type"]
    time_str = goal["reminder_time"]

    if repeat_type == "daily":
        job = schedule.every().day.at(time_str).do(
            send_notification, goal["title"]
        )

    elif repeat_type == "weekly":
        job = schedule.every().week.at(time_str).do(
            send_notification, goal["title"]
        )

    elif repeat_type == "monthly":
        job = schedule.every(30).days.at(time_str).do(
            send_notification, goal["title"]
        )

    elif repeat_type == "yearly":
        job = schedule.every(365).days.at(time_str).do(
            send_notification, goal["title"]
        )

    elif repeat_type == "custom":
        days = goal.get("custom_days", 1)
        job = schedule.every(days).days.at(time_str).do(
            send_notification, goal["title"]
        )

    elif repeat_type == "once":
        job = schedule.every().day.at(time_str).do(
            send_notification, goal["title"]
        )

    else:
        return

    scheduled_jobs[index] = job


def update_scheduler():
    goals = load_goals()

    for index, goal in enumerate(goals):

        # Smart daily reset
        reset_daily_goal(goal, index, goals)

        if not goal["completed"]:
            schedule_goal(index, goal)

    # Remove scheduled jobs for completed goals
    for index in list(scheduled_jobs.keys()):
        if index >= len(goals) or goals[index]["completed"]:
            schedule.cancel_job(scheduled_jobs[index])
            del scheduled_jobs[index]


def start_scheduler():
    print("Advanced Reminder System Running...")

    while True:
        update_scheduler()
        schedule.run_pending()
        time.sleep(1)