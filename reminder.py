from plyer import notification
import schedule
import time
from database import load_goals


def send_notification(title):
    notification.notify(
        title="Goal Reminder",
        message=f"Reminder: {title}",
        timeout=10
    )


def check_reminders():
    goals = load_goals()
    for goal in goals:
        if not goal["completed"] and goal["reminder_time"]:
            schedule.every().day.at(goal["reminder_time"]).do(
                send_notification, goal["title"]
            )


def start_scheduler():
    check_reminders()
    print("Reminder system started...")

    while True:
        schedule.run_pending()
        time.sleep(1)
