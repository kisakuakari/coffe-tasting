# database.py
import sqlite3

def get_connection():
    return sqlite3.connect("coffee.db")

def init_db():
    conn = get_connection() # DBとの繋がり全体
    cur = conn.cursor() # 実際に命令を出す係・結果を受け取る係
    # roasters（ロースター）の表（テーブル）を作ってる。
    cur.execute("""
        CREATE TABLE IF NOT EXISTS roasters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            company_name_kana TEXT,
            contact_name TEXT,
            address TEXT,
            phone TEXT,
            email TEXT,
            prefecture TEXT,
            access_token TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS coffees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roaster_id INTEGER,
            category TEXT,
            coffee_name TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS judges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            email TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            email TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_roaster(company_name, company_name_kana, contact_name,
                address, phone, email, prefecture, access_token):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO roasters
            (company_name, company_name_kana, contact_name,
             address, phone, email, prefecture, access_token)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (company_name, company_name_kana, contact_name,
         address, phone, email, prefecture, access_token)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id

def count_category_number(cur, prefix):
    cur.execute("SELECT COUNT(*) FROM coffees WHERE category = ?",
  (prefix,))
    return cur.fetchone()[0]

def add_coffee(roaster_id, category, coffee_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO coffees (roaster_id, category, coffee_name) VALUES (?, ?, ?)",
        (roaster_id, category, coffee_name)
    )
    count = count_category_number(cur, category)
    conn.commit()
    conn.close()
    return f"{category}-{count}"

def add_judge(*args, **kwargs):
    return 1

def save_score(*args, **kwargs):
    return None

# def save_coffee_number(): # その人が何個コーヒーを審査するのかを保存する関数