from pathlib import Path
from agent import dispatch_tool
from control import check_budget, run_controlled, save_events, evaluate_cases
from decisions import decide_live

ROOT = Path(__file__).resolve().parent


def main():
    result = run_controlled('Найди заметки о Python', ROOT / 'data' / 'notes.txt',
                            decide_live, {'steps': 4, 'tool_calls': 3})
    print(result)

    save_events(ROOT / 'events.jsonl', result['events'])
    print('История сохранена в events.jsonl')


if __name__ == "__main__":
    main()
