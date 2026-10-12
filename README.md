# 議事録フォーマット自動入力アプリ（gijiroku-filler）

雑なメモを貼り付けると、AI（Azure OpenAI）がメモの内容を学校指定の議事録フォーマット（Word）の各項目に振り分けて入力するアプリです。

> 🚧 開発中です。今はメモを入力する画面まで動きます。

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
- GitHub CLI（開発する場合のみ。PR の作成とマージに使います）

  ```powershell
  winget install --id GitHub.cli -e
  gh auth login
  ```

  インストールしたあとは、VS Code を開き直してから `gh` を使ってください。開き直さないと、`gh` が見つからないというエラーになります。

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

## ライブラリを追加したとき

```powershell
pip install <ライブラリ名>
pip freeze > requirements.txt
```

`pip freeze` は、今入っているライブラリの一覧を書き出すコマンドです。こうしておくと、ほかの人も同じライブラリをそろえられます。

## 開発の流れ

1つの機能を、次の流れで作ります。`main` には直接コミットしません。

```
ブランチを切る → コードを書く → /commit → /pr → main に戻る
```

| 段階 | やること |
| --- | --- |
| 1. ブランチを切る | `git switch -c feat/memo-input` のように、コミットの種類に合わせた名前で作る |
| 2. コミット | `/commit` を使う。秘密情報のチェック、メッセージの決定、コミット、プッシュまで行う |
| 3. PR とマージ | `/pr` を使う。PR を作り、マージして、ブランチを消し、`main` を `git pull` で最新にする |

PR の説明文は「概要・変更内容・動作確認・次にやること」の4つの見出しで書きます。

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
├─ README.md                  # このファイル（人間向けの説明）
├─ CLAUDE.md                  # Claude Code 用のプロジェクト説明
├─ app.py                     # 画面と全体の流れ
├─ requirements.txt           # 使っているライブラリの一覧
├─ templates/
│  └─ minutes_template.docx   # 議事録フォーマット（これから用意する）
├─ .claude/
│  ├─ rules/python.md         # Python を書くときのルール
│  └─ skills/
│     ├─ commit/SKILL.md      # コミットの手順（/commit で呼び出す）
│     └─ pr/SKILL.md          # PR の作成からマージまでの手順（/pr で呼び出す）
├─ .env.example               # .env の見本
├─ .env                       # API キーなど（Git に上げない）
├─ .gitignore                 # Git に上げないファイルの一覧
└─ .venv/                     # 仮想環境（Git に上げない）
```

### なぜこの構成にしたか

このプロジェクトは、AI（Claude Code）と一緒に開発しています。AI への指示は、**いつ読まれるか**で置き場所を分けています。

| ファイル | いつ読まれるか | 書いてあること |
| --- | --- | --- |
| `CLAUDE.md` | 毎回の作業の始めに、必ず全部読まれる | 毎回知っておく必要があること（目的、環境、守ること）。毎回読まれるので短くする |
| `.claude/rules/python.md` | Python ファイルを扱うときだけ読まれる | コードの書き方や安全のルール |
| `.claude/skills/*/SKILL.md` | `/commit` や `/pr` で呼んだときだけ読まれる | 決まった順番で進める作業の手順 |
| `README.md` | 人間が読む | アプリの説明、環境構築、開発の流れ |

こう分けた理由は2つです。

- **大事なことが埋もれないようにするため**：手順の細かいところまで `CLAUDE.md` に書くと、毎回読む量が増えます。そうすると、本当に守ってほしいルールが目立たなくなります。
- **同じ作業を毎回同じ手順で進めるため**：コミットや PR は手順をスキルにまとめているので、秘密情報のチェックや PR の書き方を毎回そろえられます。

`.env` と `.env.example` を分けているのは、API キーを Git に上げずに、どんな設定が必要かだけを共有するためです。
