from pathlib import Path
from agent import dispatch_tool
from control import check_budget, run_controlled, save_events, evaluate_cases
from decisions import decide_live

ROOT = Path(__file__).resolve().parent


def main():
    state = {'steps': 0, 'tool_calls': 0}
    limits = {'steps': 4, 'tool_calls': 3}
    events = []
    while check_budget(state, limits):
        command = decide_live('Найди заметки о Python', events)
        state['steps'] += 1
        print('Команда:', command)
        if command.get('type') == 'answer':
            if not isinstance(command.get('text'), str) or not command['text'].strip():
                raise ValueError('Модель вернула пустой ответ')
            print(command['text'])
            return
        if command.get('type') != 'tool':
            raise ValueError('Неизвестный тип команды')
        result = dispatch_tool(command, ROOT / 'data' / 'notes.txt')
        state['tool_calls'] += 1
        events.append({'command': command, 'result': result})
        print('Результат:', result)
    print('Достигнут лимит:', state)


if __name__ == "__main__":
    main()
