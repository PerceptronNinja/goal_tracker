# backend/services/goal_service.py

from backend.database.db import get_connection
from datetime import date
from backend.services.streak_service import update_streak


def create_goal(user_id, title, repeat_type, reminder_time, custom_days):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO goals
        (user_id, title, repeat_type, reminder_time, custom_days)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, title, repeat_type, reminder_time, custom_days))

    conn.commit()
    cur.close()
    conn.close()


def get_goals(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, repeat_type, reminder_time,
               current_streak, best_streak
        FROM goals
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))

    rows = cur.fetchall()

    goals = []
    for row in rows:
        goals.append({
            "id": row[0],
            "title": row[1],
            "repeat_type": row[2],
            "reminder_time": row[3],
            "current_streak": row[4],
            "best_streak": row[5],
        })

    cur.close()
    conn.close()

    return goals


def complete_goal(goal_id):
    conn = get_connection()
    cur = conn.cursor()

    today = date.today()

    # Insert completion record
    cur.execute("""
        INSERT INTO completions (goal_id, completion_date)
        VALUES (%s, %s)
    """, (goal_id, today))

    update_streak(cur, goal_id, today)

    conn.commit()
    cur.close()
    conn.close()


def delete_goal(goal_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM goals WHERE id = %s", (goal_id,))

    conn.commit()
    cur.close()
    conn.close()