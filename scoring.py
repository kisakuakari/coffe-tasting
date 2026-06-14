import pandas as pd
import random

# ============================================================
# 仮データ　← Aさんの関数ができたら差し替える
# ============================================================

def get_all_scores():
    # {coffee_id, 外観, 香り, 味わい} のリストを返す想定
    # 仮として30品 × 4人ぶんのダミーデータを作る
    scores = []
    for coffee_id in range(1, 31):      # コーヒー1〜30
        for judge_id in range(1, 5):    # 審査員4人ぶん
            scores.append({
                "coffee_id":  coffee_id,
                "judge_id":   judge_id,
                "appearance": random.randint(1, 3),   # 1〜3のランダム
                "aroma":      random.randint(1, 7),   # 1〜7のランダム
                "taste":      random.randint(1, 10),  # 1〜10のランダム
            })
    return scores

def calculate_totals():
    scores = get_all_scores()

    totals = {}

    for row in scores:
        cid = row["coffee_id"]
        point = row["appearance"] + row["aroma"] + row["taste"]

        if cid not in totals:
            totals[cid] = 0

        totals[cid] += point

    return totals

def rank_coffees():
    totals = calculate_totals()
    ranked = sorted(totals.items(),key=lambda x: x[1], reverse = True)
    return ranked

def get_winners():
    ranked = rank_coffees()
    overall_winner = ranked[0]

    return {
        "overall": overall_winner,
    }

def export_csv():
    ranked = rank_coffees()

    df = pd.DataFrame(ranked, columns=["coffee_id","合計点"])
    df["順位"] = df["合計点"].rank(method="min", ascending=False).astype(int)

    return df.to_csv(index=False)

if __name__ == "__main__":
    print("=== ランキング ===")
    for rank, (coffee_id, total) in enumerate(rank_coffees(), start=1):
        print(f"{rank}位: コーヒー{coffee_id:02d} {total}点")

    winners = get_winners()
    print(f"\n🏆 大賞: コーヒー{winners['overall'][0]:02d} ({winners['overall'][1]}点)")

    print("\n=== CSV出力確認 ===")
    print(export_csv())