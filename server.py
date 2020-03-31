import datetime
import time
from flask import Flask, request, abort

app = Flask(__name__)

messages = [
    {'username': 'Nick', 'text': 'Hello', 'time': 0.0}
]
users = {
    'Nick': '12345'
}


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/status")
def status():
    return {
        'status': True,
        'name': 'Skillbox Messenger',
        'time': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    }


@app.route("/send", methods=['POST'])
def send():
    """
    принимаем JSON
    {
        "username": str,
        "password": str,
        "text": str
    }
    :return: JSON {"ok": true}
    """
    username = request.json['username']
    password = request.json['password']

    if username in users:  # зарегистрированный пользователь
        if password != users[username]:  # авторизуем
            return abort(401)
    else:  # новый пользователь
        users[username] = password  # регистрируем

    text = request.json['text']
    current_time = time.time()
    message = {'username': username, 'text': text, 'time': current_time}
    messages.append(message)

    print(messages)

    return {"ok": True}


@app.route("/messages")
def messages_view():
    """
    принимаем ?after=float
    :return: JSON {
        "messages": [
            {"username": str, "text": str, "time": float},
            ...
        ]
    }
    """
    after = float(request.args.get('after'))

    # filtered_messages = []
    # for message in messages:
    #     if message['time'] > after:
    #         filtered_messages.append(message)

    # list comprehension:
    filtered_messages = [message for message in messages if message['time'] > after]

    return {
        'messages': filtered_messages
    }


app.run()
