import json
from assistant import extract_answer
from transport import send_live


def propose_fixture(task, old_text):
    return 'def total_price(price, quantity):\n    return price * quantity\n'


def propose_live(task, old_text):
    response = send_live([
        {'role': 'developer', 'content': 'Верни только JSON с полем new_text: полный текст исправленного prices.py. '
         'Не меняй имя и параметры функции. Не добавляй внешние действия.'},
        {'role': 'user', 'content': json.dumps({'task': task, 'file': old_text}, ensure_ascii=False)},
    ])
    result = json.loads(extract_answer(response))
    if not isinstance(result, dict) or not isinstance(result.get('new_text'), str):
        raise ValueError('Нет текста исправленного файла')
    return result['new_text']
