import requests
import json

class Misskey:
    def __init__(self, token: str):
        self.token: str = token
        self.base_url: str = 'https://misskey.io/api'

        headers: dict = {
            'Authorization': f'Bearer {self.token}'
        }
        self.session: requests.Session = requests.Session()
        self.session.headers.update(headers)

        return

    def post(self, url: str, data: dict) -> requests.Response:
        data['i'] = self.token

        return self.session.post(url, json=data)

    def follow(self, user_id: str) -> bool | dict:
        endpoint: str = self.base_url + '/following/create'
        params: dict = {
            'userId': user_id,
            "withReplies": True
        }
        response = self.post(endpoint, params)
        data = response.json()

        data['success'] = False if response.ok else True

        return data

    def unfollow(self, user_id: str) -> bool | dict:
        endpoint: str = self.base_url + '/following/delete'
        params: dict = {
            'userId': user_id
        }

        response = self.post(endpoint, params)
        return response.json() if response.ok else False

    def create_note(self, message: str, reply_id: str | None = None, channel_id: str | None = None) -> requests.Response:
        api_endpoint: str = self.base_url + '/notes/create'
        params: dict = {
            "visibility": "public",
            "visibleUserIds": [
                "string"
            ],
            "cw": None,
            "localOnly": False,
            "reactionAcceptance": None,
            "noExtractMentions": False,
            "noExtractHashtags": False,
            "noExtractEmojis": False,
            "replyId": reply_id,
            "renoteId": None,
            "channelId": channel_id,
            "text": message,
            "fileIds": None,
            "mediaIds": None,
            "poll": None,
            "scheduledAt": 0,
            "noCreatedNote": False
        }

        response = self.post(api_endpoint, params)

        return response.json() if response.ok else False
