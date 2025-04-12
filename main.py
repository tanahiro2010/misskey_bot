from lib.misskey import Misskey
from flask import *
import json

app = Flask(__name__)
misskey_client = Misskey('6PBIBfhBCqntpVF2LtgrL16Cx1joUi5c')

@app.route('/', methods=['GET', 'POST'])
def index():
    data: dict = request.json
    request_type = data['type']
    print('Event Type: {}'.format(request_type))

    if request_type == 'followed':
        user: dict = data['body']['user']
        user_id = user['id']
        user_name = user['username']
        print('Followed User_ID: {}'.format(user_id))
        print('Followed User_Name: {}'.format(user_name))

        response = misskey_client.follow(user_id)

        if response['success'] is False:
            print('Failed to follow user: {}'.format(user_id))
            misskey_client.create_note("@{} Sorry, I can't follow you right now. Please wait a little while and try again.".format(user_name))

            pass

        return {'success': response['success']}

    return json.dumps({'message': 'Hello World!'})

app.run(debug=True)