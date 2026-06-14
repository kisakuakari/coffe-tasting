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
            store TEXT,
            coffe TEXT
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

def add_coffee(id, category, coffee):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO roasters (company, email) VALUES (?, ?)",
        (company, email)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id
    return "FR-01"

def add_judge(*args, **kwargs):
    return 1

def save_score(*args, **kwargs):
    return None