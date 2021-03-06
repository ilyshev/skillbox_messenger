from flask import Flask, request, abort
from datetime import datetime
import time

app = Flask(__name__)
messages = [
    {'name': 'Jack', 'time': 10, 'text': '123'},
    {'name': 'Jack', 'time': 20, 'text': '1234'},
]
users = {
    'Jack': '12345'
}

@app.route("/")
def hello_view():
    return 'Hello, World! <a href="/status">Статус</a>'


@app.route("/status")
def status_view():
    return {
        'status': True,
        'name': 'Skillbox Messenger',
        'clients': len(users),
        'time': datetime.now().strftime('%H:%M:%S %d-%m-%Y'),
        'message': len(messages)
    }


@app.route("/send", methods=['POST'])
def send_view():
    name = request.json.get('name')
    password = request.json.get('password')
    text = request.json.get('text')

    for token in [name, password, text]:
        if not isinstance(token, str) or not token or len(token) > 1024:
            abort(400)

    if name in users:
        # auth
        if users[name] != password:
            abort(401)
    else:
        # sign up
        users[name] = password

    messages.append({'name': name, 'time': time.time(), 'text': text})
    return {'OK': True}


def filter_dicts(elements, key, min_value):
    new_elements = []

    for element in elements:
        if element[key] > min_value:
            new_elements.append(element)

    return new_elements


@app.route("/messages")
def messages_view():
    try:
        after = float(request.args['after'])
    except:
        abort(400)
    filtered_messages = filter_dicts(messages, key='time', min_value=after)
    return {'messages': filtered_messages}


app.run()