from test_functions import max_for_dicts, filter_dicts

messages = [
    {'name': 'Jack', 'time': 10, 'text': '123'},
    {'name': 'Jack', 'time': 20, 'text': '1234'},
    {'name': 'Jack', 'time': 30, 'text': '1235'},
    {'name': 'Jack', 'time': 40, 'text': '12345'},
    {'name': 'Jack', 'time': 50, 'text': '123456'}
]

print(max_for_dicts([], key='time'))
print(max_for_dicts(messages, key='time'))

print(filter_dicts([], key='time', min_value=30))
print(filter_dicts(messages, key='time', min_value=30))