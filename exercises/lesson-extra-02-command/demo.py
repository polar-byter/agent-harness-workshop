"""Проверяем текущую функцию без обращения к модели."""
import json
from io import BytesIO
from unittest.mock import patch
from decisions import build_decision_messages, parse_decision


def main():
    print('Учебная проверка без сети.')
    try:
        text = '{"type":"tool","tool":"find_notes","query":"python"}'
        print('До разбора:', type(text))
        decision = parse_decision(text)
        print('После разбора:', type(decision))
        print('Команда:', decision)
        print('Инструмент:', decision['tool'])
        print('Запрос:', decision['query'])
        for text in ('Сейчас поищу', '[]'):
            try:
                parse_decision(text)
            except ValueError as error:
                print(error)
    except NotImplementedError as error:
        print(error)


if __name__ == '__main__':
    main()
