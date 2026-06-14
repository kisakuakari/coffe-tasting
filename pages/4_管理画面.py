import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from matching import assign_coffees_to_judges, clear_assignments  # ← 追加
from scoring import rank_coffees, get_winners, export_csv
from collections import Counter

# ============================================================
# 関所
# ============================================================
pw = st.text_input("管理パスワード", type="password")
if pw != "coffee2026":
    st.stop()

# ============================================================
# 仮データ　← Aさんの関数ができたら差し替える
# ============================================================
def get_summary():
    return {
        "roasters": 12,
        "coffees":  30,
        "judges":   10,
        "scores":   48,
    }

def get_ranking_with_name():
    categories = ["フルーティー", "フローラル", "ナッティ",
                  "チョコレート", "スパイシー", "シトラス"]
    prefixes   = ["FR", "FL", "NT", "CH", "SP", "CT"]

    ranked = rank_coffees()

    rows = []
    for coffee_id, total in ranked:
        idx      = (coffee_id - 1) % 6
        prefix   = prefixes[idx]
        num      = ((coffee_id - 1) // 6) + 1
        name     = f"{prefix}-{num:02d}"
        category = categories[idx]
        rows.append({
            "コーヒー": name,
            "部門":     category,
            "合計点":   total,
        })
    return rows

# ============================================================
# タイトル
# ============================================================
st.title("運営管理画面")
st.caption("Coffee Tasting Contest 2026 — 現在の状況")

# ============================================================
# ① 現在の状況
# ============================================================
summary = get_summary()

col1, col2, col3, col4 = st.columns(4)
col1.metric("ロースター数", f"{summary['roasters']} 社")
col2.metric("出品コーヒー", f"{summary['coffees']} 品")
col3.metric("審査員数",     f"{summary['judges']} 名")
col4.metric("採点済み",     f"{summary['scores']} 件")

st.divider()

# ============================================================
# ② 割り当て状況
# ============================================================
st.subheader("割り当て状況")

if "reviewers" not in st.session_state:
    st.session_state.reviewers = None

if st.session_state.reviewers:
    reviewers     = st.session_state.reviewers
    counts        = list(reviewers.values())
    diff          = max(counts) - min(counts)
    count_summary = Counter(counts)
    base          = max(count_summary, key=count_summary.get)
    less_count    = count_summary.get(base - 1, 0)

    col1, col2, col3 = st.columns(3)
    col1.metric("基本担当数",      f"{base} 人")
    col2.metric(f"{base-1}人担当", f"{less_count} 品")
    col3.metric("最大差",          f"{diff} 人")

    if diff <= 1:
        st.success("公平性 OK — 最大差1人")
    else:
        st.warning(f"最大差 {diff}人 — 要確認")

else:
    st.info("まだ割り当てが実行されていません")

N = st.number_input("1人あたりの審査数", min_value=1, value=12)

col_btn1, col_btn2, _ = st.columns([1, 1, 3])
with col_btn1:
    if st.button("割り当て実行", type="primary"):
        reviewers = assign_coffees_to_judges(N=N)  # DBにも保存される
        st.session_state.reviewers = reviewers
        st.rerun()

with col_btn2:
    if st.button("再割り当て"):
        clear_assignments()                # ← DBの割り当てを全削除
        st.session_state.reviewers = None
        st.rerun()

st.divider()

# ============================================================
# ③ ランキング
# ============================================================
st.subheader("ランキング（上位5件）")

rows    = get_ranking_with_name()
df_rank = pd.DataFrame(rows)

df_rank["順位"] = df_rank["合計点"].rank(
    method="min", ascending=False
).astype(int)

df_rank = df_rank[["順位", "コーヒー", "部門", "合計点"]]

st.dataframe(df_rank.head(5), hide_index=True)

with st.expander("全件表示"):
    st.dataframe(df_rank, hide_index=True)

csv = export_csv()
st.download_button(
    label="CSVダウンロード",
    data=csv,
    file_name="result.csv",
    mime="text/csv",
)