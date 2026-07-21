import sqlite3

DB = "users.db"

def connect():
    return sqlite3.connect(DB)

# Создание таблицы
def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        tariff TEXT DEFAULT 'Wi-Fi',
        link TEXT DEFAULT ''
    )
    """)

    conn.commit()
    conn.close()

# Добавить пользователя
def add_user(user_id, username):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO users
        (user_id, username)
        VALUES (?, ?)
        """,
        (user_id, username)
    )

    conn.commit()
    conn.close()

# Выдать тариф
def set_tariff(user_id, tariff, link):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET tariff=?, link=?
        WHERE user_id=?
        """,
        (tariff, link, user_id)
    )

    conn.commit()
    conn.close()

# Получить пользователя
def get_user(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )

    user = cur.fetchone()

    conn.close()
    return user

# Получить всех пользователей
def get_all_users():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")

    users = cur.fetchall()

    conn.close()
    return users

# Забрать Обход Б/С
def remove_bs(user_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET tariff='Wi-Fi',
            link=''
        WHERE user_id=?
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()