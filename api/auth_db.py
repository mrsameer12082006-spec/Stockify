import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "database",
    "users.db"
)


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_users_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        created_at TEXT

    )
    """)

    conn.commit()
    conn.close()


def create_user(email, password):
    """Create a user with email + hashed password.

    Uses a derived display name to remain compatible with the current table schema
    that includes a required `name` column.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        inferred_name = email.split("@")[0] if "@" in email else email
        cursor.execute(
            """
            INSERT INTO users (name, email, password, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (inferred_name, email, password, datetime.now()),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM users WHERE email = ?
        """,
        (email,),
    )
    user = cursor.fetchone()
    conn.close()
    return user


def get_user(email):
    """Return user tuple in (id, email, password, created_at) order."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, email, password, created_at
        FROM users
        WHERE email = ?
        """,
        (email,),
    )
    user = cursor.fetchone()
    conn.close()
    return user