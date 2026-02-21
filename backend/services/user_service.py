# backend/services/user_service.py

import bcrypt
from backend.database.db import get_connection


def register_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cur.execute("""
            INSERT INTO users (username, password_hash)
            VALUES (%s, %s)
            RETURNING id
        """, (username, hashed_password.decode()))

        user_id = cur.fetchone()[0]
        conn.commit()
    except Exception:
        conn.rollback()
        user_id = None

    cur.close()
    conn.close()

    return user_id


def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, password_hash
        FROM users
        WHERE username = %s
    """, (username,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return None

    user_id, stored_hash = user

    if bcrypt.checkpw(password.encode(), stored_hash.encode()):
        return user_id

    return None