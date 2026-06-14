import random
import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "coffee.db")


def init_temp_db():
    """暫定用。init_db()ができたら削除する"""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            judge_id  INTEGER NOT NULL,
            coffee_id INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_all_coffees():
    return list(range(1,31))

def get_all_judges():
    return list(range(1,11))

def clear_assignments():
    conn = get_connection()
    conn.execute("DELETE FROM assignments")
    conn.commit()
    conn.close()

def save_assignment(judge_id,coffee_id):
    conn = get_connection()
    conn.execute(
        "INSERT INTO assignments (judge_id, coffee_id) VALUES (?, ?)",
        (judge_id, coffee_id)
    )
    conn.commit()
    conn.close()

def get_assignments_for_judge(judge_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT coffee_id FROM assignments WHERE judge_id = ?",
        (judge_id,)
    ).fetchall()
    conn.close()
    return [row[0] for row in rows]  

def assign_coffees_to_judges(N=12):
    coffees = get_all_coffees()
    judges = get_all_judges()
    random.shuffle(judges)

    total = len(judges)*N
    base = total // len(coffees)
    extra = total % len(coffees)

    remaining = {}
    for coffee in coffees :
          remaining[coffee] = base

    for i in range(extra):
          remaining[coffees[i]] += 1

    reviewers = {}
    for coffee in coffees:
          reviewers[coffee] = 0

    for judge in judges:
        ranked = sorted(coffees , key=lambda c: remaining[c], reverse=True)
        chosen = ranked[:N]

        for coffee in chosen:
            save_assignment(judge,coffee)
            remaining[coffee] -= 1
            reviewers[coffee] += 1
    return reviewers

if __name__ == "__main__":
    init_temp_db() #testyou
    result = assign_coffees_to_judges(N=12)

    print("=== 各コーヒーの審査員数 ===")
    for coffee_id, count in result.items():
        print(f"コーヒー{coffee_id:02d}: {count}人")

    diff = max(result.values()) - min(result.values())
    print(f"\n最大差: {diff}人")