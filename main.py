from lib.writecream import WriteCream
from lib.misskey import Misskey
from dotenv import load_dotenv
from flask import *
import json
import os
from datetime import datetime

load_dotenv('.env.local')

app = Flask(__name__)
misskey_client = Misskey(os.getenv('API_KEY'))
writecream_client = WriteCream()
self_data = misskey_client.get_conf()

def log(message: str) -> None:
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} -> {message}")

@app.route('/', methods=['GET', 'POST'])
def index():
    data: dict = request.json
    request_type = data['type']
    log(f"Event Type: {request_type}")

    with open('sample.json', 'w') as f:
        f.write(json.dumps(data, indent=2))

    if request_type == 'followed':
        user: dict = data['body']['user']
        user_id = user['id']
        user_name = user['username']
        log(f"Followed User_ID: {user_id}")
        log(f"Followed User_Name: {user_name}")

        response: dict = misskey_client.follow(user_id)

        if response['success'] is False:
            log(f"Failed to follow user: {user_id}")
            misskey_client.create_note(f"@{user_name} Sorry, I can't follow you right now. Please wait a little while and try again.")
        else:
            log(f"Success to follow user: {user_id}")

        return {'success': response['success']}

    if request_type == 'mention':
        note = data['body']['note']
        note_id: str = note['id']
        note_user: dict = note['user']
        note_content: str = note['text']
        note_reply: str | None = note['replyId']
        father_note: dict | None = None

        log(f"From User_ID: {note_user['id']}")
        log(f"From User_Name: {note_user['name']}")
        log(f"Note Content: {note_content}")
        log(f"Note Reply: {note_reply}")

        if note_reply is not None:
            log("  Reply is Defined")
            father_note = misskey_client.get_note(note_reply)
            father_content = father_note['text']
            log(f"  Note Father_Content: {father_content}")
            note_content = f"{father_content}\n\n{note_content}"

        response: str | None = writecream_client.ask(client_name=note_user['name'], message=note_content.replace(f"@{self_data['username']}", ''))

        if response is None:
            log("  Failed to ask question")
            send_response = misskey_client.create_note(
                f"@{note_user['username']}, Sorry, I can't answer that question. ({'Defined' if father_note else 'UnDefined'} Father)",
                reply_id=note_id
            )

            if send_response:
                log("    Success to send error message.")
            else:
                log("    Failed to send error message.")
            return

        print(response)

        send_response = misskey_client.create_note(f"@{note_user['username']} {response}", reply_id=note_id)
        if send_response:
            log("    Success to send message.")
        else:
            log("    Failed to send message.")

    return json.dumps({'message': 'Hello World!'})

def main():
    if self_data is None:
        log("Failed to get self data.")
        log("  Auth failed. please change token.")
        return

    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

if __name__ == '__main__':
    main()
