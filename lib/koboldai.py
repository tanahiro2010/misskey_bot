import requests
import json
import time

class Koboldai:
    def __init__(self):
        self.base_url = "https://aihorde.net/api/v2/generate/text"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 New Browser'})

        return

    def get_answer(self, uuid: str) -> str | None:
        url: str = f"{self.base_url}/status/{uuid}"
        while True:
            response = self.session.get(url)
            if response.ok:
                result = response.json()
                if result['generations'] and result['generations'][0]['text']:
                    return str(result['generations'][0]['text'])

                print('Continue...')
                time.sleep(2)
                continue
            else:
                break

        return None
    def ask(self, message: str) -> str | None:
        url: str = f"{self.base_url}/async"
        data: dict = {
            "prompt": f"\n### Instruction:\n{message}\n### Response:\n",
            "params": {
                "n": 1,
                "max_context_length": 1800,
                "max_length": 200,
                "rep_pen": 1.07,
                "temperature": 0.75,
                "top_p": 0.92,
                "top_k": 100,
                "top_a": 0,
                "typical": 1,
                "tfs": 1,
                "rep_pen_range": 360,
                "rep_pen_slope": 0.7,
                "sampler_order": [6, 0, 1, 3, 4, 2, 5],
                "use_default_badwordsids": False,
                "stop_sequence": [
                    "### Instruction:",
                    "### Response:"
                ],
                "min_p": 0,
                "dynatemp_range": 0,
                "dynatemp_exponent": 1,
                "smoothing_factor": 0,
                "nsigma": 0
            },
            "models": [
                "koboldcpp/Cydonia-v1.3-Magnum-v4-22B",
                "koboldcpp/gemma-3-1b-it",
                "koboldcpp/gemma-3-4b-it",
                "koboldcpp/Gemmasutra-Mini-2B-v1",
                "koboldcpp/google_gemma-3-1b-it-Q4_K_M",
                "koboldcpp/L3-8B-Stheno-v3.2",
                "koboldcpp/Meta-Llama-3-8B-Instruct",
                "koboldcpp/mini-magnum-12b-v1.1",
                "koboldcpp/TheDrummer_Fallen-Gemma3-27B-v1-Q4_K_L",
                "tabbyAPI/Behemoth-123B-v1.2-4.0bpw-h6-exl2"
            ],
            "workers": []
        }
        headers = {
            'ApiKey': '0000000000'  # ここに本物のAPIキーを入れてください
        }
        response = self.session.post(url, json=data, headers=headers)
        try:
            body: dict = response.json()

            if response.ok:
                uuid = body['id'] if body else None
                if uuid is None:
                    return 'uuid is undefined'

                return self.get_answer(uuid)

        except json.decoder.JSONDecodeError:
            return response.text


        return None
