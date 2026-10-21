"""Получаем исходный ответ сервиса, пока его статистика ещё доступна."""
from time import perf_counter

from assistant import build_messages, extract_answer
from transport import course_response, read_connection, request_json


def collect_usage(provider: str, response: dict, elapsed_seconds: float) -> dict:
    stats = {
        'input_tokens': None,
        'output_tokens': None,
        'cached_tokens': None,
        'elapsed_seconds': elapsed_seconds,
        'generation_seconds': None,
        'output_tokens_per_second': None,
        'requested_context_tokens': None,
    }
    if provider == 'ollama':
        stats['input_tokens'] = response.get('prompt_eval_count')
        stats['output_tokens'] = response.get('eval_count')
        stats['cached_tokens'] = response.get('prompt_eval_cached_count')
        stats['requested_context_tokens'] = 4096
        duration = response.get('eval_duration')
        if isinstance(duration, (int, float)) and duration > 0:
            seconds = duration / 1_000_000_000
            stats['generation_seconds'] = seconds
            count = stats['output_tokens']
            if isinstance(count, (int, float)):
                stats['output_tokens_per_second'] = count / seconds
    else:
        usage = response.get('usage') or {}
        stats['input_tokens'] = usage.get('prompt_tokens')
        stats['output_tokens'] = usage.get('completion_tokens')
        details = usage.get('prompt_tokens_details') or {}
        stats['cached_tokens'] = details.get('cached_tokens')
    return stats


def request_sample(question: str, notes: list[str]) -> tuple[str, dict]:
    messages = build_messages(question, notes)
    prepared = [dict(message, role='system') if message.get('role') == 'developer'
                else dict(message) for message in messages]
    settings = read_connection()
    provider = settings['provider']
    if provider == 'ollama':
        url = 'http://127.0.0.1:11434/api/chat'
        payload = {
            'model': settings['model'], 'messages': prepared, 'stream': False,
            'think': False, 'options': {'num_gpu': 0, 'num_ctx': 4096, 'num_predict': 1200},
        }
    else:
        urls = {'openrouter': 'https://openrouter.ai/api/v1/chat/completions',
                'vsegpt': 'https://api.vsegpt.ru/v1/chat/completions'}
        url = urls[provider]
        payload = {'model': settings['model'], 'messages': prepared,
                   'stream': False, 'max_tokens': 1200}
    started = perf_counter()
    response = request_json(url, payload, settings.get('api_key', ''))
    elapsed_seconds = perf_counter() - started
    if provider == 'ollama':
        if not response.get('done') or response.get('done_reason') != 'stop':
            raise ValueError('Модель не завершила ответ; проверьте лимит генерации')
        text = response.get('message', {}).get('content')
    else:
        choices = response.get('choices') or []
        if not choices or choices[0].get('finish_reason') != 'stop':
            raise ValueError('Сервис не завершил ответ; проверьте лимит генерации')
        text = choices[0].get('message', {}).get('content')
    answer = extract_answer(course_response(text))
    return answer, collect_usage(provider, response, elapsed_seconds)
