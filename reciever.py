import time
import datetime
import requests


def get_messages(after):
    response = requests.get(
        'http://127.0.0.1:5000/messages',
        params={'after': after}
    )
    data = response.json()
    return data['messages']


def print_message(message):
    username = message['username']
    message_time = message['time']
    text = message['text']

    dt = datetime.datetime.fromtimestamp(message_time)
    dt_beauty = dt.strftime('%H:%M:%S')

    print(dt_beauty, username)
    print(text)
    print()


after = 0

while True:
    messages = get_messages(after)

    if messages:
        after = messages[-1]['time']
        for message in messages:
            print_message(message)

    time.sleep(2)
