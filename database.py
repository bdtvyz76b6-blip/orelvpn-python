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

        wifi_active INTEGER DEFAULT 1,
        bs_active INTEGER DEFAULT 0,

        wifi_link TEXT DEFAULT '',
        bs_link TEXT DEFAULT '',

        payment_status TEXT DEFAULT 'none'
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


# Выдать Обход Б/С
def activate_bs(user_id, link):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users

        SET
        bs_active=1,
        bs_link=?,
        payment_status='approved'

        WHERE user_id=?
        """,
        (link, user_id)
    )

    conn.commit()
    conn.close()


# Забрать Обход Б/С
def remove_bs(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users

        SET
        bs_active=0,
        bs_link=''

        WHERE user_id=?
        """,
        (user_id,)
    )

    conn.commit()
    conn.close()


# Получить пользователя
def get_user(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM users
        WHERE user_id=?
        """,
        (user_id,)
    )

    user = cur.fetchone()

    conn.close()

    return user



# Все пользователи для админки
def get_all_users():

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM users
        ORDER BY user_id DESC
        """
    )

    users = cur.fetchall()

    conn.close()

    return users