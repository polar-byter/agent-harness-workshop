"""Проверяем текущую функцию без обращения к модели."""
import json
from io import BytesIO
from unittest.mock import patch
from decisions import build_decision_messages, parse_decision


def main():
    print('Учебная проверка без сети.')
    try:
        for events in ([], [{'tool': 'find_notes', 'result': ['Python lists keep item order.']}]):
            messages = build_decision_messages('Найди заметки о Python', events)
            for message in messages:
                print(message['role'] + ': ' + message['content'])
    except NotImplementedError as error:
        print(error)


if __name__ == '__main__':
    main()
