import threading
from database import add_goal, load_goals, mark_completed, delete_goal
from reminder import start_scheduler


def view_goals():
    goals = load_goals()

    if not goals:
        print("\nNo goals found.")
        return

    print("\nYour Goals:")
    for i, goal in enumerate(goals):
        status = "✅" if goal["completed"] else "❌"
        print(
            f"{i+1}. {goal['title']} | {goal['type']} | "
            f"Reminder: {goal['reminder_time']} | {status}"
        )


def create_goal():
    title = input("Enter goal title: ")
    goal_type = input("Daily / Monthly / Yearly: ")
    reminder_time = input("Reminder time (HH:MM 24hr format or leave blank): ")

    if reminder_time.strip() == "":
        reminder_time = None

    add_goal(title, goal_type, reminder_time)
    print("Goal added successfully!")


def complete_goal():
    view_goals()
    index = int(input("Select goal number to mark completed: ")) - 1

    if mark_completed(index):
        print("Goal marked as completed!")
    else:
        print("Invalid selection.")


def remove_goal():
    view_goals()
    index = int(input("Select goal number to delete: ")) - 1

    if delete_goal(index):
        print("Goal deleted!")
    else:
        print("Invalid selection.")


def main():
    # Start reminder scheduler in background
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()

    while True:
        print("\n===== GOAL TRACKER =====")
        print("1. Add Goal")
        print("2. View Goals")
        print("3. Mark Completed")
        print("4. Delete Goal")
        print("5. Exit")

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
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
