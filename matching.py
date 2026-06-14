# ============================================================
# 仮データ　←　Aさんの関数ができたら、この2つを差し替えるだけ
# ============================================================

def  get_all_coffees():
    return list(range(1,31))

def get_all_judges():
    return list(range(1,11))

def save_assignment(judge_id,coffee_id):
    pass


def assign_coffees_to_judges(N=12):
    coffees = get_all_coffees()
    judges = get_all_judges()
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
    result = assign_coffees_to_judges(N=12)

    print("=== 各コーヒーの審査員数 ===")
    for coffee_id, count in result.items():
        print(f"コーヒー{coffee_id:02d}: {count}人")

    # 最大差チェック
    diff = max(result.values()) - min(result.values())
    print(f"\n最大差: {diff}人　←　1以下なら成功ですわ")