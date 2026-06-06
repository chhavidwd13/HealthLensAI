import sqlite3


def create_history_table():

    conn = sqlite3.connect("healthlens.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        activity TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_activity(username, activity):

    conn = sqlite3.connect("healthlens.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO history(username, activity)
        VALUES (?,?)
        """,
        (username, activity)
    )

    conn.commit()
    conn.close()


def get_user_history(username):

    conn = sqlite3.connect("healthlens.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT activity
        FROM history
        WHERE username=?
        ORDER BY id DESC
        """,
        (username,)
    )

    data = cursor.fetchall()

    conn.close()

    return data