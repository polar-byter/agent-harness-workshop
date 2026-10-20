"""Connect the course functions to the reader's chosen model."""
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def connection_path() -> Path:
    override = os.environ.get('HARNESS_CONNECTION_FILE')
    if override:
        return Path(override)
    folder = Path(os.environ.get('LOCALAPPDATA', Path.home() / '.config'))
    return folder / 'AgentHarnessWorkshop' / 'connection.json'


def read_connection() -> dict:
    path = connection_path()
    if not path.is_file():
        raise ValueError('Подключение не настроено. Запустите configure_model.py из урока подключения.')
    settings = json.loads(path.read_text(encoding='utf-8'))
    if settings.get('provider') not in ('openrouter', 'vsegpt', 'ollama'):
        raise ValueError('Выберите OpenRouter, VseGPT или Ollama в configure_model.py')
    if not isinstance(settings.get('model'), str) or not settings['model'].strip():
        raise ValueError('В настройках отсутствует имя модели')
    if settings['provider'] != 'ollama' and not settings.get('api_key'):
        raise ValueError('Для сервиса нужен API-ключ. Откройте configure_model.py')
    return settings


def send_fixture(messages: list[dict]) -> dict:
    path = Path(__file__).resolve().parent / 'data' / 'response.json'
    return json.loads(path.read_text(encoding='utf-8'))


def request_json(url: str, payload: dict, api_key: str = '') -> dict:
    headers = {'Content-Type': 'application/json'}
    if api_key:
        headers['Authorization'] = 'Bearer ' + api_key
    request = Request(url, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
                      headers=headers, method='POST')
    try:
        with urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as error:
        hints = {401: 'Проверьте API-ключ.', 402: 'Проверьте баланс или пробные кредиты.',
                 403: 'Проверьте доступность модели для аккаунта и региона.',
                 404: 'Проверьте имя модели; для Ollama сначала выполните ollama pull.',
                 429: 'Лимит запросов или временная перегрузка. Повторите позже.'}
        raise ValueError(f'Сервис вернул HTTP {error.code}. ' + hints.get(error.code, 'Проверьте состояние сервиса.')) from None
    except (URLError, TimeoutError):
        raise ValueError('Нет ответа от модели. Для Ollama проверьте, что приложение запущено; для API - соединение.') from None


def course_response(text: str) -> dict:
    if not isinstance(text, str) or not text.strip():
        raise ValueError('Модель не вернула текст ответа')
    return {'status': 'completed', 'output': [
        {'type': 'message', 'content': [{'type': 'output_text', 'text': text}]}
    ]}


def send_live(messages: list[dict]) -> dict:
    if not isinstance(messages, list):
        raise ValueError('send_live ожидает список сообщений, без обёртки в словарь')
    settings = read_connection()
    # These backends accept the course's developer instructions as a system message.
    prepared = [dict(message, role='system') if message.get('role') == 'developer'
                else dict(message) for message in messages]
    if settings['provider'] == 'ollama':
        response = request_json('http://127.0.0.1:11434/api/chat', {
            'model': settings['model'], 'messages': prepared, 'stream': False,
            'think': False, 'options': {'num_gpu': 0, 'num_ctx': 4096, 'num_predict': 1200},
        })
        if not response.get('done') or response.get('done_reason') != 'stop':
            raise ValueError('Локальная модель не завершила ответ; проверьте размер запроса и лимит генерации')
        return course_response(response.get('message', {}).get('content'))
    urls = {'openrouter': 'https://openrouter.ai/api/v1/chat/completions',
            'vsegpt': 'https://api.vsegpt.ru/v1/chat/completions'}
    response = request_json(urls[settings['provider']], {
        'model': settings['model'], 'messages': prepared, 'stream': False, 'max_tokens': 1200,
    }, settings['api_key'])
    choices = response.get('choices', [])
    if not choices or choices[0].get('finish_reason') != 'stop':
        raise ValueError('Сервис не завершил текстовый ответ; проверьте модель и лимит генерации')
    return course_response(choices[0].get('message', {}).get('content'))
