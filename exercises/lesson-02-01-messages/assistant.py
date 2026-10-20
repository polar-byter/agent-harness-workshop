import json
from pathlib import Path


def build_messages(question: str, notes: list[str]) -> list[dict]:
    if not question.strip():
        raise ValueError('Вопрос не должен быть пустым')
    data = {'question': question, 'notes': notes}
    content = json.dumps(data, ensure_ascii=False)
    raise NotImplementedError("Допишите build_messages по подсказкам урока")


def extract_answer(response: dict) -> str:
    raise NotImplementedError("Допишите extract_answer по подсказкам урока")


def answer_question(question: str, notes: list[str], send) -> str:
    raise NotImplementedError("Допишите answer_question по подсказкам урока")
