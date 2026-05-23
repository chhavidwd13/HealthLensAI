import sqlite3
import hashlib


DB_NAME = "users.db"


def create_users_table():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


def hash_password(password):

    return hashlib.sha256(password.encode()).hexdigest()


def signup_user(username, password):

    try:
        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        hashed_password = hash_password(password)

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        conn.commit()
        conn.close()

        return True

    except:
        return False


def login_user(username, password):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hashed_password)
    )

    data = cursor.fetchone()

    conn.close()

    return data