# コーヒー品評会システム 実装ガイド（Python + Streamlit + SQLite）

## 0. 全体の地図（ファイル構成）

```
coffee_contest/
├── app.py                  # トップページ（入口）
├── database.py             # DBの接続・テーブル作成・データの読み書き
├── matching.py             # コーヒーを審査員に配るロジック
├── scoring.py              # 点数の集計・ランキング・CSV出力
├── utils.py                # 秘密URLのトークン作りなど便利関数
├── pages/                  # Streamlitは pages/ の中身を自動でメニューにする
│   ├── 1_ロースター申込.py
│   ├── 2_審査員申込.py
│   ├── 3_審査フォーム.py
│   └── 4_管理画面.py
└── coffee.db               # 自動で作られるデータベースファイル
```

**考え方：**
- `pages/` の中の各ファイル = 1つの画面（Webページ）
- `database.py` など = 画面から呼び出す「部品（関数）」を置く場所
- 画面ファイルは「見た目」を作り、計算や保存は部品の関数に任せる

---

## 1. database.py に作る関数（データの出入り口）

ここに作った関数を、全部の画面が呼び出して使います。

| 関数名 | 何をする | 受け取る | 返す |
|--------|----------|----------|------|
| `get_connection()` | coffee.db につなぐ | なし | 接続 |
| `init_db()` | テーブルを5つ作る（無ければ） | なし | なし |
| `add_roaster(社名, 担当者, メール, ...)` | ロースターを登録 | 入力内容 | roaster_id |
| `add_coffee(roaster_id, 部門, ...)` | 出品コーヒーを登録＋番号付け | 内容 | コーヒー番号(例 FR-01) |
| `add_judge(氏名, メール, ...)` | 審査員を登録＋番号付け | 内容 | 審査員番号(例 001) |
| `get_roaster_by_email(メール)` | メールでロースターを探す | メール | ロースター情報 |
| `get_judge_by_email(メール)` | メールで審査員を探す | メール | 審査員情報 |
| `get_coffees_by_roaster(roaster_id)` | そのロースターのコーヒー一覧 | id | コーヒーのリスト |
| `save_score(審査員id, コーヒーid, 外観, 香り, 味)` | 点数を保存 | 点数 | なし |
| `get_all_scores()` | 全部の点数を取り出す | なし | 点数のリスト |

**テーブルは5つ：** `roasters`（ロースター）, `coffees`（コーヒー）, `judges`（審査員）, `assignments`（誰が何を審査するか）, `scores`（点数）

---

## 2. utils.py に作る関数（便利な小物）

| 関数名 | 何をする |
|--------|----------|
| `make_token(メール)` | メールから秘密のURL用の長い文字列を作る（`hashlib`を使う） |
| `next_coffee_number(部門)` | その部門の次の番号を計算（FR-01の次はFR-02） |
| `next_judge_number()` | 次の審査員番号を計算（001→002） |

> `next_coffee_number` と `next_judge_number` は `database.py` に入れてもOK。番号付けは「今いくつまであるか数えて＋1」するだけです。

---

## 3. matching.py に作る関数（コーヒーを配る）

| 関数名 | 何をする |
|--------|----------|
| `assign_coffees_to_judges()` | ①全コーヒーをシャッフル ②審査員に均等に配る ③`assignments`テーブルに保存 |
| `get_assignments_for_judge(審査員id)` | その審査員が担当するコーヒー一覧を返す |

**均等配分のコツ（小学生向け）：**
コーヒーをトランプのように配ります。1枚ずつ「次の審査員、次の審査員…」と順番に配れば自然と人数がそろいます。最後に「どのコーヒーも審査員数の差が10人以内か」を確認します。

---

## 4. scoring.py に作る関数（集計）

| 関数名 | 何をする |
|--------|----------|
| `calculate_totals()` | コーヒーごとに点数を合計する |
| `rank_coffees()` | 合計点の高い順に並べる |
| `get_winners()` | 全体の大賞＋部門ごとの金賞を決める |
| `export_csv()` | 結果をCSVファイルにして出す |

**点数の範囲：** 外観 1〜3 / 香り 1〜7 / 味わい 1〜10 → 合計 3〜20点

---

## 5. データの流れ（どう連携するか）

```
[ロースター申込画面] --add_roaster()--> coffee.db
                     --add_coffee()---> coffee.db（FR-01などの番号がつく）

[審査員申込画面]    --add_judge()-----> coffee.db（001などの番号がつく）

[管理画面のボタン]  --assign_coffees_to_judges()--> assignmentsに保存

[審査フォーム画面]  --get_assignments_for_judge()--> 担当コーヒー表示
                    --save_score()----------------> scoresに保存

[管理画面]          --rank_coffees() / get_winners()--> 結果表示
                    --export_csv()-----------------> CSV出力
```

ポイント：**画面は関数を呼ぶだけ。中身の処理は関数の中。** だから画面ファイルは短くてシンプルになります。

---

## 6. 実装の順番（30分ごと）

### STEP 0: 準備（30分）
- [ ] `coffee_contest` フォルダを作る
- [ ] `pip install streamlit` する
- [ ] `app.py` に「Hello」と表示し、`streamlit run app.py` で動かす

### STEP 1: database.py の土台（30分）
- [ ] `get_connection()` を書く
- [ ] `init_db()` でテーブル5つを作る
- [ ] `app.py` の最初で `init_db()` を1回呼ぶ → coffee.db ができるか確認

### STEP 2: ロースター申込（30分×2）
- [ ] `database.py` に `add_roaster()` `add_coffee()` を書く
- [ ] `next_coffee_number()` で番号付け（FR-01…）
- [ ] `pages/1_ロースター申込.py` で入力欄を作り、送信で上の関数を呼ぶ

### STEP 3: 審査員申込（30分×2）
- [ ] `database.py` に `add_judge()`、`next_judge_number()` を書く
- [ ] `pages/2_審査員申込.py` で入力欄＋送信（ラベルは日英併記）

### STEP 4: 秘密URL／簡易ログイン（30分）
- [ ] `utils.py` に `make_token()` を書く
- [ ] 申込後にトークンURLを表示
- [ ] メール入力でマイページに入れるようにする（`get_..._by_email`）

### STEP 5: マッチング（30分×2）
- [ ] `matching.py` に `assign_coffees_to_judges()` を書く
- [ ] `pages/4_管理画面.py` に「割り当て実行」ボタンを置いて呼ぶ
- [ ] 各コーヒーの審査員数を表示して、差が10人以内か確認

### STEP 6: 審査フォーム（30分×2）
- [ ] `matching.py` に `get_assignments_for_judge()` を書く
- [ ] `pages/3_審査フォーム.py` で担当コーヒーを表示
- [ ] 外観・香り・味のスライダー → 送信で `save_score()`

### STEP 7: 集計・結果（30分×2）
- [ ] `scoring.py` に `calculate_totals()` `rank_coffees()` `get_winners()`
- [ ] `pages/4_管理画面.py` にランキングと受賞を表示

### STEP 8: CSV出力（30分）
- [ ] `scoring.py` に `export_csv()`
- [ ] 管理画面に `st.download_button` でダウンロードボタンを付ける

---

## 困ったときの順番
1. まず STEP 0〜1 を必ず動かす（DBができれば半分成功）
2. 1画面ずつ「保存できた」を確認しながら進める
3. 全部つながってから、見た目を整える