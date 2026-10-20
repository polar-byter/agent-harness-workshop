import json
from pathlib import Path
from agent import dispatch_tool


def check_budget(state: dict, limits: dict) -> bool:
    for name in ('steps', 'tool_calls'):
        if type(state.get(name)) is not int or state[name] < 0:
            raise ValueError('Неверный счётчик: ' + name)
        if type(limits.get(name)) is not int or limits[name] < 1:
            raise ValueError('Неверный лимит: ' + name)
    return state['steps'] < limits['steps'] and state['tool_calls'] < limits['tool_calls']


def select_context(task: str, events: list[dict], max_events: int) -> dict:
    if type(max_events) is not int or max_events < 0:
        raise ValueError('max_events должен быть неотрицательным целым')
    recent = events[-max_events:] if max_events else []
    return {'task': task, 'events': recent}


def save_events(path: Path, events: list[dict]) -> None:
    with path.open('w', encoding='utf-8') as stream:
        for event in events:
            stream.write(json.dumps(event, ensure_ascii=False) + '\n')


def evaluate_cases(cases: list[dict], run) -> dict:
    results = []
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
