# 議事録フォーマット自動入力アプリ（gijiroku-filler）

雑なメモを貼り付けると、AI（Azure OpenAI）がメモの内容を学校指定の議事録フォーマット（Word）の各項目に振り分けて入力するアプリです。

> 🚧 開発中です。今は環境構築まで終わっています。

## しくみ

```
メモ → AI が5項目に振り分け（JSON） → Python の辞書 → docxtpl でテンプレートに流し込み → Word を出力
```

| 項目 | 内容 |
| --- | --- |
| date | 日時 |
| attendees | 参加者 |
| agenda | 議題 |
| decisions | 決定事項 |
| todos | 次回までの課題 |

- AI はメモにない内容を追加しません。
- メモにない項目は空欄にして「⚠️ 未記入」と表示します。

## 使っている技術

| ライブラリ | 役割 |
| --- | --- |
| [Streamlit](https://streamlit.io/) | 画面を作る |
| [openai](https://pypi.org/project/openai/) | Azure OpenAI を呼び出す |
| [docxtpl](https://docxtpl.readthedocs.io/) | Word テンプレートの目印（`{{ date }}` など）に値を入れる |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | `.env` から API キーなどを読み込む |

## 環境構築（Windows / PowerShell）

### 0. 必要なもの

- Python 3.12（`py -0` を実行して `-V:3.12` が表示されれば入っています）
- Git
- Azure OpenAI のリソース（エンドポイント、API キー、デプロイ名）

### 1. プロジェクトを手元に用意する

```powershell
git clone <このリポジトリのURL>
cd gijiroku-filler
```

### 2. 仮想環境を作る

仮想環境は、このプロジェクト専用のライブラリ置き場です。ほかのプロジェクトのライブラリと混ざらないようにするために使います。

```powershell
py -3.12 -m venv .venv
```

Python のバージョンが 3.12 になるように、`-3.12` を付けています。

### 3. 仮想環境を有効にする（作業前に毎回）

```powershell
.venv\Scripts\activate
```

行の先頭に `(.venv)` と表示されれば成功です。

### 4. ライブラリを入れる

```powershell
pip install -r requirements.txt
```

`requirements.txt` には、このアプリで使うライブラリとそのバージョンが書いてあります。

### 5. API キーを設定する

1. `.env.example` をコピーして、`.env` という名前のファイルを作ります。

   ```powershell
   Copy-Item .env.example .env
   ```

2. `.env` を開き、`<...>` の部分を自分の Azure OpenAI の値に書き換えます。

⚠️ `.env` は秘密情報なので Git に上げません（`.gitignore` で除外しています）。

### 6. アプリを起動する

```powershell
streamlit run app.py
```

ブラウザでアプリが開きます。終了するときは、PowerShell で `Ctrl + C` を押します。

> `app.py` はまだ作っていません。

## ライブラリを追加したとき

```powershell
pip install <ライブラリ名>
pip freeze > requirements.txt
```

`pip freeze` は、今入っているライブラリの一覧を書き出すコマンドです。こうしておくと、ほかの人も同じライブラリをそろえられます。

## うまくいかないとき

### `activate` で「スクリプトの実行が無効」と表示される

PowerShell の設定で、スクリプトの実行が止められています。次のコマンドを一度だけ実行すると、自分のユーザーだけ実行できるようになります。

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### `pip install` で「別のプロセスが使用中です」と表示される

VS Code やウイルス対策ソフトがファイルを開いていると起こることがあります。いったん VS Code を閉じ、次の手順で仮想環境を作り直してください。

```powershell
Remove-Item -Recurse -Force .venv
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## フォルダ構成

```
gijiroku-filler/
├─ README.md                  # このファイル
├─ CLAUDE.md                  # Claude Code 用のプロジェクト説明
├─ app.py                     # 画面と全体の流れ（これから作る）
├─ requirements.txt           # 使っているライブラリの一覧
├─ templates/
│  └─ minutes_template.docx   # 議事録フォーマット（これから用意する）
├─ .env.example               # .env の見本
├─ .env                       # API キーなど（Git に上げない）
├─ .gitignore                 # Git に上げないファイルの一覧
└─ .venv/                     # 仮想環境（Git に上げない）
```
