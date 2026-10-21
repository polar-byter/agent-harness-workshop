import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent


def send_fixture(messages: list[dict]) -> dict:
    """Читаем подготовленный ответ из файла без обращения к модели."""
    return json.loads((ROOT / 'data' / 'response.json').read_text(encoding='utf-8'))


def send_live(messages: list[dict]) -> dict:
    key = os.environ.get('OPENAI_API_KEY')
    model = os.environ.get('OPENAI_MODEL')
    if not key or not model:
        raise ValueError('Укажите OPENAI_API_KEY и OPENAI_MODEL в настройках запуска')
    payload = {'model': model, 'input': messages, 'max_output_tokens': 1200}
    request = Request('https://api.openai.com/v1/responses',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'},
        method='POST')
    with urlopen(request, timeout=40) as response:
        return json.loads(response.read().decode('utf-8'))
