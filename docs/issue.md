いいと思う。この設計なら、**4人で「画面担当」ではなく「機能の層」で分ける**のが安全です。理由は、Streamlit の画面はすぐ書けるけど、DB・番号付け・マッチング・集計がバラバラに実装されると後で地獄を見るからです。小規模ハッカソンあるあるの沼です。

仕様上も、ロースター・審査員の登録、ランダム均等割当、審査フォーム、管理画面での結果表示/CSVが中心なので、この4分担がきれいです。仕様書ではローカル動作でよく、クラウド不要とされています。また、マッチングは「全出品コーヒーをランダムに審査員へ配分し、各コーヒーの審査員数の幅を最大10人以内にする」ルールです。

## まず結論：4人の分担

### Aさん：DB・共通関数担当

担当ファイル：

```txt
database.py
utils.py
coffee.db
```

やること：

```txt
get_connection()
init_db()
add_roaster()
add_coffee()
add_judge()
get_roaster_by_email()
get_judge_by_email()
get_coffees_by_roaster()
save_score()
get_all_scores()
make_token()
next_coffee_number()
next_judge_number()
```

この人が一番「土台」です。
他の3人はこの人の関数を呼ぶだけにします。

最初に作るべきテーブル：

```txt
roasters
coffees
judges
assignments
scores
```

注意点は、**関数名と返り値を先に決めること**。中身が仮でもいいので、まず他の人が使える形を作る。

例：

```python
def add_judge(name, email, prefecture, address, phone, workplace):
    # TODO: DB保存
    return judge_id
```

---

### Bさん：ロースター申込画面担当

担当ファイル：

```txt
pages/1_ロースター申込.py
```

呼ぶ関数：

```txt
add_roaster()
add_coffee()
get_roaster_by_email()
make_token()
```

やること：

```txt
ロースター基本情報の入力フォーム
出品コーヒーの入力フォーム
部門選択 FR / FL / NT / CH / SP / CT
送信ボタン
登録完了メッセージ
秘密URLっぽいものを表示
```

ここは画面担当だけど、**DBに直接SQLを書かない**のが大事です。

画面側ではこういう感じにする：

```python
roaster_id = add_roaster(company_name, contact_name, email, ...)
coffee_number = add_coffee(roaster_id, category, roast_level, ...)
```

---

### Cさん：審査員申込・審査フォーム担当

担当ファイル：

```txt
pages/2_審査員申込.py
pages/3_審査フォーム.py
```

呼ぶ関数：

```txt
add_judge()
get_judge_by_email()
get_assignments_for_judge()
save_score()
make_token()
```

やること：

```txt
審査員登録フォーム
審査員番号 001, 002... の表示
メール入力で簡易ログイン
担当コーヒー一覧の表示
外観 1〜3
香り 1〜7
味わい 1〜10
点数保存
```

審査フォームは仕様の核です。
ただし、マッチングがまだできていない間は、仮の担当コーヒーを表示して先にUIを作ってOKです。

たとえば最初は：

```python
assignments = [
    {"coffee_id": 1, "coffee_number": "FR-01", "category": "フルーティー"},
    {"coffee_id": 2, "coffee_number": "CH-01", "category": "チョコレート"},
]
```

で画面だけ作っておく。

---

### Dさん：マッチング・集計・管理画面担当

担当ファイル：

```txt
matching.py
scoring.py
pages/4_管理画面.py
```

呼ぶ/作る関数：

```txt
assign_coffees_to_judges()
get_assignments_for_judge()
calculate_totals()
rank_coffees()
get_winners()
export_csv()
```

やること：

```txt
管理画面
割り当て実行ボタン
割り当て結果の確認
各コーヒーの審査員数表示
ランキング表示
Coffee of the Year 表示
部門別金賞表示
CSVダウンロード
```

この人はややロジック重め。
特に `assignments` テーブルの作り方はAさんと相談が必要です。

---

## OSが違う問題：最初に全員で揃えるルール

Ubuntu / mac / Windows が混ざるなら、**環境構築で時間を溶かさないルール**を先に決めた方がいいです。

### 推奨ルール

全員これで統一：

```bash
python -m venv .venv
```

起動方法だけOS別にする。

Ubuntu / mac：

```bash
source .venv/bin/activate
```

Windows PowerShell：

```powershell
.venv\Scripts\Activate.ps1
```

インストール：

```bash
pip install -r requirements.txt
```

起動：

```bash
streamlit run app.py
```

`requirements.txt` は最初はこれだけでOK：

```txt
streamlit
pandas
```

SQLiteはPython標準なので、基本的に追加インストール不要です。

---

## Gitの運用：これがかなり大事

4人で同じファイルを触ると衝突します。
だから、担当ファイルをなるべく分けます。

### ブランチ例

```txt
feature/db-foundation
feature/roaster-form
feature/judge-and-score-form
feature/admin-matching-scoring
```

### 最初にmainへ入れるべきもの

まずAさん、または全員で、最低限の空ファイルを作ってmainに入れる。

```txt
app.py
database.py
utils.py
matching.py
scoring.py
pages/1_ロースター申込.py
pages/2_審査員申込.py
pages/3_審査フォーム.py
pages/4_管理画面.py
requirements.txt
.gitignore
README.md
```

`.gitignore` はこれ：

```gitignore
.venv/
__pycache__/
*.pyc
coffee.db
.DS_Store
```

**coffee.db はGitに入れない**方がいいです。
各自のローカルで `init_db()` して作る。

---

## 実装順はこうすると詰まりにくい

### 第1フェーズ：全員で30分

全員同じところを確認します。

```txt
1. リポジトリ作成
2. venv作成
3. requirements.txtでインストール
4. streamlit run app.py が全員のOSで動く
5. init_db() で coffee.db が作れる
```

ここで誰かが動かないまま進むと、後で爆発します。
ここだけは全員で同期。

---

### 第2フェーズ：AさんがDBの仮APIを作る

中身が完全じゃなくても、関数の形だけ先に作る。

```python
def add_roaster(*args, **kwargs):
    return 1

def add_coffee(*args, **kwargs):
    return "FR-01"

def add_judge(*args, **kwargs):
    return 1

def save_score(*args, **kwargs):
    return None
```

これでB/C/Dさんが画面を先に作れます。

---

### 第3フェーズ：B/C/Dさんが並行作業

```txt
B: ロースター申込画面
C: 審査員申込画面 + 審査フォーム
D: 管理画面 + マッチング仮実装 + 集計仮実装
```

この段階では、DBが未完成でも仮データで進めてOKです。

---

### 第4フェーズ：接続テスト

1画面ずつ確認します。

```txt
ロースター登録できる
コーヒー番号 FR-01 がつく
審査員登録できる
審査員番号 001 がつく
管理画面で割り当てできる
審査フォームに担当コーヒーが出る
点数保存できる
ランキングが出る
CSVが出る
```

この順番がいいです。

---

## 4人の作業表

| 人 | 主担当           | 触るファイル                                         | 他の人との依存                                        |
| - | ------------- | ---------------------------------------------- | ---------------------------------------------- |
| A | DB・共通関数       | `database.py`, `utils.py`                      | 全員がAの関数を使う                                     |
| B | ロースター申込       | `pages/1_ロースター申込.py`                           | Aの `add_roaster`, `add_coffee`                 |
| C | 審査員申込・審査フォーム  | `pages/2_審査員申込.py`, `pages/3_審査フォーム.py`        | Aの `add_judge`, Dの `get_assignments_for_judge` |
| D | 管理画面・マッチング・集計 | `matching.py`, `scoring.py`, `pages/4_管理画面.py` | AのDB設計、Cの審査データ                                 |

---

## 当日の合言葉

**「画面にSQLを書かない」**
**「DBファイルはGitに入れない」**
**「まず保存できたら勝ち」**
**「見た目は最後」**

この規模なら、最初から完璧な設計を狙うより、
`登録 → 割当 → 採点 → 集計` の一本線を最速で通すのがいちばん強いです。
