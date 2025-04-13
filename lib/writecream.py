import urllib.parse
import requests
import json


class WriteCream:
    def __init__(self):
        self.base_url = 'https://8pe3nv3qha.execute-api.us-east-1.amazonaws.com/default/llm_chat?'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
        })

        return

    def encode_to_url_params(self, data: dict) -> str:
        # ネストされた構造はJSON文字列に変換する
        encoded_data = {}
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                encoded_data[key] = json.dumps(value)
            else:
                encoded_data[key] = str(value)

        # URLエンコードされたクエリ文字列を作成
        return urllib.parse.urlencode(encoded_data)

    def ask(self, client_name: str, message: str) -> str | None:
        data: dict = {
            "query": [
                {"role": "system", "content": "You are a helpful and informative AI assistant.Client's name is {}".format(client_name)},
                {"role": "user", "content": message}
            ],
            'link': 'writecream.com',
        }

        endpoint: str = self.base_url + self.encode_to_url_params(data)
        response: requests.Response = self.session.get(endpoint)

        if response.ok:
            return response.json()['response_content']

        return None


if __name__ == '__main__':
    client = WriteCream()
    print(client.ask('あなたの名前を教えてください.'))