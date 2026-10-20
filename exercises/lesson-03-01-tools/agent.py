import json
from pathlib import Path
from notes import find_notes, read_notes


def dispatch_tool(command: dict, notes_path: Path) -> dict:
    name = command.get('tool')
    raise NotImplementedError("Допишите dispatch_tool по подсказкам урока")


def run_agent(task: str, notes_path: Path, decide, max_steps: int = 4) -> dict:
    raise NotImplementedError("Допишите run_agent по подсказкам урока")


def decide_fixture(task: str, events: list[dict]) -> dict:
    if not events:
        return {'type': 'tool', 'tool': 'find_notes', 'query': 'python'}
    return {'type': 'answer', 'text': 'Найдены две заметки о Python.'}
