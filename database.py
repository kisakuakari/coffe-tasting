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
            category TEXT,           -- 部門の接頭辞 (FR, FL, NT, CH, SP, CT)
            coffee_number TEXT,      -- 自動採番 (例 FR-01)
            coffee_name TEXT,        -- コーヒー名
            roast_level INTEGER,     -- 焙煎度
            acidity INTEGER,         -- 酸味
            body INTEGER,            -- ボディ
            sweetness INTEGER,       -- 甘味
            retail_price INTEGER,    -- 小売価格(税込)
            annual_roast_kg REAL,    -- 年間焙煎量(kg換算)
            roast_date TEXT,         -- 焙煎日
            package_size TEXT        -- 販売パッケージサイズ
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

def add_coffee(roaster_id, category, coffee_name, roast_level, acidity, body, sweetness, retail_price, annual_roast_kg, roast_date, package_size):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO coffees (roaster_id, category, coffee_name, roast_level, acidity, body, sweetness, retail_price, annual_roast_kg, roast_date, package_size) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (roaster_id, category, coffee_name, roast_level, acidity, body, sweetness, retail_price, annual_roast_kg, roast_date, package_size)
    )
    count = count_category_number(cur, category)
    cur.execute(
        "INSERT INTO coffees (coffee_number) VALUES (?)",
        (f"{category}-{count}")
    )
    conn.commit()
    conn.close()
    return f"{category}-{count}"

def add_judge(*args, **kwargs):
    return 1

def save_score(*args, **kwargs):
    return None

# def save_coffee_number(): # その人が何個コーヒーを審査するのかを保存する関数