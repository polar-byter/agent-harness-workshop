import json
from pathlib import Path
from agent import dispatch_tool


def check_budget(state: dict, limits: dict) -> bool:
    steps = state.get('steps')
    tool_calls = state.get('tool_calls')
    raise NotImplementedError("Допишите check_budget по подсказкам урока")


def select_context(task: str, events: list[dict], max_events: int) -> dict:
    raise NotImplementedError("Допишите select_context по подсказкам урока")


def save_events(path: Path, events: list[dict]) -> None:
    raise NotImplementedError("Допишите save_events по подсказкам урока")


def evaluate_cases(cases: list[dict], run) -> dict:
    raise NotImplementedError("Допишите evaluate_cases по подсказкам урока")


def run_controlled(task, notes_path, decide, limits, max_events=2):
    state = {'steps': 0, 'tool_calls': 0}
    events = []
    while check_budget(state, limits):
        context = select_context(task, events, max_events)
        command = decide(context['task'], context['events'])
        state['steps'] += 1
        if command.get('type') == 'answer':
            if not isinstance(command.get('text'), str) or not command['text'].strip():
                raise ValueError('Пустой ответ')
            return {'status': 'completed', 'answer': command['text'], 'events': events, 'state': state}
        if command.get('type') != 'tool':
            raise ValueError('Ожидался ответ или инструмент')
        result = dispatch_tool(command, notes_path)
        state['tool_calls'] += 1
        events.append({'command': command, 'result': result})
    return {'status': 'budget_limit', 'answer': '', 'events': events, 'state': state}
