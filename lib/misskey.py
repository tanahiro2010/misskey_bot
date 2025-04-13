import requests
import json
from typing import Optional, Union

class Misskey:
    def __init__(self, token: str, host: str = 'misskey.io'):
        """
        Misskey API クライアントを初期化します。

        :param token: Misskey API トークン
        :param host: Misskey インスタンスのホスト名（デフォルトは misskey.io）
        """
        self.token = token
        self.base_url = f'https://{host}/api'

        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.token}'
        })

    def post(self, endpoint: str, data: dict) -> requests.Response:
        """
        POST リクエストを送信します。

        :param endpoint: API エンドポイント（base_url からの相対パス）
        :param data: リクエストボディのデータ
        :return: レスポンスオブジェクト
        """
        data['i'] = self.token
        return self.session.post(endpoint, json=data)

    def get_conf(self) -> Optional[dict]:
        """
        自身のアカウント情報を取得します。

        :return: アカウント情報の辞書、失敗時は None
        """
        response = self.post(f'{self.base_url}/i', {})
        return response.json() if response.ok else None

    def follow(self, user_id: str) -> dict:
        """
        指定したユーザーをフォローします。

        :param user_id: フォロー対象ユーザーのID
        :return: API のレスポンスに success を追加した辞書
        """
        endpoint = f'{self.base_url}/following/create'
        params = {
            'userId': user_id,
            'withReplies': True
        }
        response = self.post(endpoint, params)
        data = response.json() if response.ok else {}
        data['success'] = response.ok
        return data

    def unfollow(self, user_id: str) -> dict:
        """
        指定したユーザーのフォローを解除します。

        :param user_id: フォロー解除対象ユーザーのID
        :return: API のレスポンスに success を追加した辞書
        """
        endpoint = f'{self.base_url}/following/delete'
        params = {
            'userId': user_id
        }
        response = self.post(endpoint, params)
        data = response.json() if response.ok else {}
        data['success'] = response.ok
        return data

    def create_note(self, message: str, reply_id: Optional[str] = None, channel_id: Optional[str] = None) -> Union[dict, bool]:
        """
        ノート（投稿）を作成します。

        :param message: 投稿する本文
        :param reply_id: 返信対象ノートのID（省略可）
        :param channel_id: 投稿するチャンネルID（省略可）
        :return: 成功時はレスポンス辞書、失敗時は False
        """
        endpoint = f'{self.base_url}/notes/create'
        params = {
            "visibility": "public",
            "text": message
        }

        if reply_id:
            params["replyId"] = reply_id
        if channel_id:
            params["channelId"] = channel_id

        response = self.post(endpoint, params)
        return response.json() if response.ok else False

    def get_note(self, note_id: str) -> Optional[dict]:
        """
        指定したノートの詳細を取得します。

        :param note_id: ノートID
        :return: ノートの情報、失敗時は None
        """
        endpoint = f'{self.base_url}/notes/show'
        params = {
            'noteId': note_id
        }
        response = self.post(endpoint, params)
        return response.json() if response.ok else None
