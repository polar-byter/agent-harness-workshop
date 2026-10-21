"""Проверяем текущую функцию без обращения к модели."""
import json
from io import BytesIO
from unittest.mock import patch
from decisions import build_decision_messages, parse_decision


def main():
    print('Учебная проверка без сети.')
    try:
        for events in ([], [{'tool': 'find_notes', 'result': ['Возврат товара возможен в течение 14 дней.']}]):
            messages = build_decision_messages('Найди в регламенте пункты о возврате', events)
            for message in messages:
                print(message['role'] + ': ' + message['content'])
    except NotImplementedError as error:
        print(error)


if __name__ == '__main__':
    main()
