# misskey_bot

[@tanahiro2010_dev](https://misskey.io/@tanahiro2010_dev) <br />
This account is run the program.

# 🐦 Misskey API Python クライアント(lib/misskey,py)

Misskey.io の API を操作するための Python クラスです。  
Botアカウントからノート投稿・フォロー・アンフォロー・ノート取得・自アカウント情報の取得が可能です。

---

## 🔧 クラス初期化

```python
from lib.misskey import Misskey

misskey = Misskey(token='YOUR_ACCESS_TOKEN', host='misskey.io')
```

- `token` : 発行済みアクセストークン（文字列）
- `host` : Misskeyのホスト(デフォルトはmisskey.io)

---

## 📡 共通メソッド

### `post(url: str, data: dict) -> requests.Response`

内部用メソッド。APIリクエストの共通化。全てのリクエストに `i`（アクセストークン）を付加して送信します。

---

## 📋 API 操作メソッド

---

### 🧑‍💼 `get_conf() -> dict | None`

アクセストークンに紐づいた **自アカウント情報** を取得します。

```python
info = misskey.get_conf()
```

---

### ➕ `follow(user_id: str) -> dict`

指定ユーザーをフォローします。

```python
result = misskey.follow(user_id='xxxxxxxxxxxx')
if result['success']:
    print('フォロー成功')
```

- 成功時: `{"success": True, ...}`
- 失敗時: `{"success": False, "error": ...}`

---

### ➖ `unfollow(user_id: str) -> dict`

指定ユーザーのフォローを解除します。

```python
result = misskey.unfollow(user_id='xxxxxxxxxxxx')
if result['success']:
    print('アンフォロー成功')
```

- 戻り値は `follow()` と同じ形式。

---

### 📝 `create_note(message: str, reply_id: str | None = None, channel_id: str | None = None) -> dict | bool`

ノート（投稿）を作成します。

```python
note = misskey.create_note("こんにちは、Misskey！")
```

- `reply_id`: リプライ対象のノートID（任意）
- `channel_id`: 投稿先チャンネルID（任意）
- 成功時: ノート情報の `dict`
- 失敗時: `False`

---

### 🔍 `get_note(note_id: str) -> dict | None`

指定IDのノートを取得します。

```python
note = misskey.get_note(note_id='xxxxxxxxxxxx')
```

- 成功時: ノート情報の `dict`
- 失敗時: `None`

---

## 📦 依存ライブラリ

- `requests`

```bash
pip install requests
```

---
