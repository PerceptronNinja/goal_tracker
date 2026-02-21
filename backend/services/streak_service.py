# backend/services/streak_service.py

def update_streak(cur, goal_id, today):

    cur.execute("""
        SELECT last_completed_date, current_streak, best_streak
        FROM goals
        WHERE id = %s
    """, (goal_id,))

    row = cur.fetchone()

    last_date, current_streak, best_streak = row

    if last_date:
        delta = (today - last_date).days
    else:
        delta = None

    if delta == 1:
        current_streak += 1
    elif delta == 0:
        return
    else:
        current_streak = 1

    best_streak = max(best_streak, current_streak)

    cur.execute("""
        UPDATE goals
        SET current_streak = %s,
            best_streak = %s,
            last_completed_date = %s
        WHERE id = %s
    """, (current_streak, best_streak, today, goal_id))