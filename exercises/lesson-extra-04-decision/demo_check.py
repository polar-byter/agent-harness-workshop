"""Проверяем текущую функцию без обращения к модели."""
import json
from io import BytesIO
from unittest.mock import patch
from decisions import build_decision_messages, parse_decision


def main():
    print('Учебная проверка без сети.')
    try:
        from decisions import decide_live
        from transport import course_response
        text = '{"type":"tool","tool":"find_notes","query":"python"}'
        with patch('decisions.send_live', return_value=course_response(text)):
            print(decide_live('Найди заметки о Python', []))
    except NotImplementedError as error:
        print(error)


if __name__ == '__main__':
    main()
