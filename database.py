# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect("coffee.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS roasters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            email TEXT
        )
    """)
    # 同じように coffees / judges / assignments / scores も作る
    conn.commit()
    conn.close()

def add_roaster(*args, **kwargs):
    return 1

def add_coffee(*args, **kwargs):
    return "FR-01"

def add_judge(*args, **kwargs):
    return 1

def save_score(*args, **kwargs):
    return None