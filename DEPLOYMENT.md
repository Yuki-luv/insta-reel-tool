# 🌐 初心者向け：ツール公開手順書 (GitHub + Streamlit Cloud)

この手順通りに進めれば、作成した「リール動画生成ツール」をインターネット上で公開し、取引先と共有できます。
（黒い画面や難しいコマンドは使いません！すべてブラウザ上で完結します）

---

## 🟢 ステップ1: GitHub（ギットハブ）の準備
ソースコードを保存する「場所」を作ります。

1. [GitHub.com](https://github.com/) にアクセスし、右上の「Sign up」から無料アカウントを作成します。
2. ログイン後、画面右上の「＋」アイコン → 「**New repository**」をクリック。
3. 設定画面で以下を入力：
   - **Repository name**: `insta-reel-tool` （好きな名前でOK）
   - **Public / Private**: `Private`（非公開）を選ぶと安全ですが、Streamlit Cloudとの連携時に承認などが必要になることがあります。一番簡単なのは `Public` ですが、パスワード制限をかけているので安心してください。今回は **Public** で進めましょう。
   - 「Add a README file」にチェックを入れる。
4. 「**Create repository**」ボタンをクリック。
5. 「箱」ができました！

---

## 🟢 ステップ2: ファイルのアップロード
作った「箱」に、パソコンにあるツールのファイルを入れます。

1. パソコンで `insta-reel-generator` フォルダを開きます。
2. 以下のファイル・フォルダを選びます（Ctrlキーを押しながらクリック）：
   - `app.py`
   - `config.py`
   - `video_utils.py`
   - `packages.txt`
   - `requirements.txt`
   - `assets` フォルダ（まるごと）
   - `DEPLOYMENT.md` (このファイル)
   
   ⚠️注意: `.git` フォルダや `output` フォルダ、`__pycache__` は不要です。

3. GitHubの画面に戻り、「**Add file**」→「**Upload files**」をクリック。
4. さきほど選んだファイルを、画面の枠内にドラッグ＆ドロップします。
   （アップロードが終わるまで少し待ちます）
5. 下の方にある「**Commit changes**」ボタンをクリック。

これでコードがネット上に保存されました！

---

## 🟢 ステップ3: Streamlit Cloud で公開
いよいよアプリを動かします。

1. [Streamlit Community Cloud](https://streamlit.io/cloud) にアクセス。
2. 「Sign up with GitHub」を選んでログイン。
3. 「**New app**」ボタンをクリック。
4. 「Use existing repo」を選択。
5. **Repository**: さきほど作った `あなたのID/insta-reel-tool` を選択。
6. **Main file path**: `app.py` と入力されているはずです（そのまま）。
7. 「**Deploy!**」ボタンをクリック！

---

## � ステップ4: アプリの確認とパスワード設定
デプロイボタンを押すと、「Oven is cooking...（準備中）」のような画面になり、数分後にアプリが起動します。

1. **パスワード設定**:
   - 初期設定ではパスワードは `1234` です。
   - これを変えたい場合は、Streamlit Cloudの管理画面（Appの設定）で `Secrets` という項目を探し、以下のように書きます：
     ```toml
     password = "好きなパスワード"
     ```
   - これで保存すると、そのパスワード以外では入れなくなります。

2. **共有**:
   - アプリが開いているブラウザの **URL（https://...streamlit.app）** をコピーします。
   - これを取引先にメールやLINEで送るだけ！
   - 「パスワードは 1234 です」と一言添えてください。

---

## 🔄 今後の更新方法
BGMを追加したり、設定を変えたいときは？

1. **GitHub** のページを開きます。
2. `assets/bgm` フォルダなどをクリックして進みます。
3. 右上の「Add file」→「Upload files」から新しいBGMを追加し、「Commit changes」を押します。
4. すると、Streamlit Cloud が自動的に変更を検知して、数分後にアプリも更新されます！

以上です。やってみてください！
