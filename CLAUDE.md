# 議事録フォーマット自動入力アプリ（gijiroku-filler）

学校指定の議事録フォーマット（Word）に、雑なメモの内容を振り分けて埋めるアプリ。
就職・インターン選考用のポートフォリオとして作っている。

## 私について

- プログラミング未経験。Pythonの基本（変数・リスト／辞書・if・for・関数）を学び始めたところ。
- 目標は「自分のコードを日本語で説明できること」。少しずつ、説明付きで進めたい。
- プログラミング技術もある程度身に着けたいためコードはなるべく手書きしたい

## 環境

- Windows / PowerShell / Python 3.12
- 仮想環境：`.venv`（コマンドは必ずWindows用を使う）

## よく使うコマンド

```powershell
.venv\Scripts\activate              # 仮想環境を有効にする（作業前に毎回）
pip install <ライブラリ名>           # ライブラリを追加する
pip freeze > requirements.txt       # 使っているライブラリを記録する
streamlit run app.py                # アプリを起動する
```

## アーキテクチャ

メモ → AI（Azure OpenAI）で5項目のJSONに振り分け → Pythonの辞書 → docxtplでテンプレートに流し込み → Word出力

- 項目名：date（日時）, attendees（参加者）, agenda（議題）, decisions（決定事項）, todos（次回までの課題）
- AIはメモにない内容を追加しない。ない項目は空にして「⚠️ 未記入」と表示する

## ディレクトリ構成

```
gijiroku-filler/
├─ CLAUDE.md                  # このファイル（セッション開始時の情報）
├─ README.md                  # 人間向けの説明・環境構築手順
├─ app.py                     # 画面（Streamlit）と全体の流れ
├─ templates/
│  └─ minutes_template.docx   # 目印 {{ date }} などを入れた議事録フォーマット
├─ .claude/
│  ├─ rules/python.md         # コードを書くときのルール
│  └─ skills/commit/SKILL.md  # コミット手順（/commit で呼び出す）
├─ .env                       # APIキーなど（Gitに上げない）
├─ .gitignore
└─ .venv/                     # 仮想環境（Gitに上げない）
```

`.env`、`.venv/`、`templates/` 内のWordファイルは、私が頼まない限り変更しない。

## セッション開始時の手順

1. `git status` で、前回の作業の続きか、未コミットの変更がないかを確認する
2. 今回やることを1つだけ私と確認してから始める
3. 環境構築の詳しい手順は README.md を参照する
4. 1つの機能を作るたびに新たなブランチを切って開始する（ブランチを切ったら報告）。ブランチ名は `.claude/skills/commit/SKILL.md` のコミットメッセージの種類に合わせる（例：`feat/memo-input`）
