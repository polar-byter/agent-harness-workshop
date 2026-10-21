"""Проверяем текущую функцию без обращения к модели."""
import json
from io import BytesIO
from unittest.mock import patch
from decisions import build_decision_messages, parse_decision


def main():
    print('Учебная проверка без сети.')
    try:
        from transport import request_json
        def reply(request, timeout):
            print(request.get_method(), request.full_url)
            print(json.loads(request.data.decode('utf-8')))
            return BytesIO(b'{"ok": true}')
        with patch('transport.urlopen', side_effect=reply):
            print(request_json('https://example.invalid/chat',
                               {'model': 'учебная-модель', 'messages': [], 'stream': False}))
    except NotImplementedError as error:
        print(error)


if __name__ == '__main__':
    main()
