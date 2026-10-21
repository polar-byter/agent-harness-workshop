from contextlib import contextmanager
import re
from pathlib import Path


@contextmanager
def load_model(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f'Положите файл модели сюда: {path}')
    from llama_cpp import Llama
    model = Llama(
        model_path=str(path), n_ctx=2048, n_gpu_layers=0,
        seed=42, verbose=False,
    )
    try:
        yield model
    finally:
        model.close()


def prepare_messages(messages: list[dict]) -> list[dict]:
    prepared = []
    for message in messages:
        item = dict(message)
        if item['role'] == 'developer':
            item['role'] = 'system'
            # Режим короткого ответа Qwen; правило ответа по заметкам сохраняется.
            item['content'] += ' Ответь кратко по-русски. /no_think'
        prepared.append(item)
    return prepared


def convert_response(response: dict) -> dict:
    choice = response['choices'][0]
    if choice.get('finish_reason') != 'stop':
        raise ValueError('Генерация не завершена: проверьте лимит max_tokens')
    text = choice['message'].get('content')
    if not isinstance(text, str):
        raise ValueError('Модель не вернула текст')
    # Qwen может поставить служебный блок перед окончательным ответом.
    text = re.sub(r'\A\s*<think>.*?</think>\s*', '', text, flags=re.S).strip()
    if not text:
        raise ValueError('Модель не вернула окончательный ответ')
    return {'status': 'completed', 'output': [
        {'type': 'message', 'content': [{'type': 'output_text', 'text': text}]}
    ]}
