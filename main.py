import threading
from database import add_goal, load_goals, mark_completed, delete_goal
from reminder import start_scheduler
from datetime import datetime
import calendar


# ----------------------------
# View Goals (Updated Schema)
# ----------------------------
def view_goals():
    goals = load_goals()

    if not goals:
        print("\nNo goals found.")
        return

    print("\n===== YOUR GOALS =====")
    for i, goal in enumerate(goals):
        status = "✅" if goal["completed"] else "❌"

        print(
            f"{i+1}. {goal['title']} | "
            f"{goal.get('repeat_type', 'daily')} | "
            f"Reminder: {goal['reminder_time']} | "
            f"Streak: {goal.get('current_streak', 0)} | "
            f"Best: {goal.get('best_streak', 0)} | "
            f"{status}"
        )


# ----------------------------
# Create Goal
# ----------------------------
def create_goal():
    title = input("Enter goal title: ")

    print("\nRepeat Types:")
    print("1. Daily")
    print("2. Weekly")
    print("3. Monthly")
    print("4. Yearly")
    print("5. Custom (every X days)")
    print("6. One-time")

    choice = input("Choose repeat type: ")

    mapping = {
        "1": "daily",
        "2": "weekly",
        "3": "monthly",
        "4": "yearly",
        "5": "custom",
        "6": "once"
    }

    repeat_type = mapping.get(choice, "daily")

    reminder_time = input("Reminder time (HH:MM 24hr): ")

    custom_days = None
    if repeat_type == "custom":
        custom_days = int(input("Repeat every how many days? "))

    add_goal(title, repeat_type, reminder_time, custom_days)

    print("Goal added successfully!")


# ----------------------------
# Mark Goal Completed
# ----------------------------
def complete_goal():
    view_goals()
    try:
        index = int(input("Select goal number to mark completed: ")) - 1
    except ValueError:
        print("Invalid input.")
        return

    if mark_completed(index):
        print("Goal marked as completed!")
    else:
        print("Invalid selection.")


# ----------------------------
# Delete Goal
# ----------------------------
def remove_goal():
    view_goals()
    try:
        index = int(input("Select goal number to delete: ")) - 1
    except ValueError:
        print("Invalid input.")
        return

    if delete_goal(index):
        print("Goal deleted!")
    else:
        print("Invalid selection.")


# ----------------------------
# Analytics
# ----------------------------
def show_analytics():
    goals = load_goals()

    total = len(goals)
    completed = sum(1 for g in goals if g["completed"])

    if total == 0:
        print("No goals available.")
        return

    completion_rate = (completed / total) * 100
    longest_streak = max((g.get("best_streak", 0) for g in goals), default=0)

    print("\n===== ANALYTICS =====")
    print(f"Total Goals: {total}")
    print(f"Completed Goals: {completed}")
    print(f"Completion Rate: {completion_rate:.2f}%")
    print(f"Longest Streak: {longest_streak}")


# ----------------------------
# Calendar Tracking
# ----------------------------
def show_calendar():
    goals = load_goals()
    now = datetime.now()

    print("\n===== MONTH CALENDAR =====")

    for goal in goals:
        print(f"\nGoal: {goal['title']}")
        completed_days = goal.get("history", [])

        cal = calendar.monthcalendar(now.year, now.month)

        for week in cal:
            for day in week:
                if day == 0:
                    print("   ", end=" ")
                else:
                    date_str = f"{now.year}-{now.month:02d}-{day:02d}"
                    if date_str in completed_days:
                        print("✅", end="  ")
                    else:
                        print("• ", end=" ")
            print()


# ----------------------------
# AI Goal Suggestion (Basic)
# ----------------------------
def ai_goal_suggestion():
    focus = input("What do you want to improve? (fitness/study/mindset): ")

    suggestions = {
        "fitness": [
            "Walk 8000 steps daily",
            "Workout 30 minutes daily",
            "Drink 3L water daily"
        ],
        "study": [
            "Study 2 hours daily",
            "Revise weekly",
            "Solve 10 practice problems daily"
        ],
        "mindset": [
            "Read 10 pages daily",
            "Meditate 15 minutes daily",
            "Journal every night"
        ]
    }

    print("\nAI Suggestions:")
    for s in suggestions.get(focus.lower(), ["No suggestions found."]):
        print("-", s)


# ----------------------------
# Main Loop
# ----------------------------
def main():
    scheduler_thread = threading.Thread(
        target=start_scheduler,
        daemon=True
    )
    scheduler_thread.start()

    while True:
        print("\n===== GOAL TRACKER =====")
        print("1. Add Goal")
        print("2. View Goals")
        print("3. Mark Completed")
        print("4. Delete Goal")
        print("5. View Analytics")
        print("6. View Calendar")
        print("7. AI Goal Suggestion")
        print("8. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            create_goal()
        elif choice == "2":
            view_goals()
        elif choice == "3":
            complete_goal()
        elif choice == "4":
            remove_goal()
        elif choice == "5":
            show_analytics()
        elif choice == "6":
            show_calendar()
        elif choice == "7":
            ai_goal_suggestion()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()