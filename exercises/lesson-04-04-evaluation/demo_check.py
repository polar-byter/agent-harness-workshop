import json
import hashlib
from pathlib import Path
from notes import find_notes, find_notes_alt, read_notes
from assistant import build_messages, extract_answer, answer_question
from transport import send_fixture
from agent import dispatch_tool, run_agent, decide_fixture
from control import check_budget, select_context, save_events, evaluate_cases, run_controlled

ROOT = Path(__file__).resolve().parent


def main():
    print('Учебный запуск без обращения к модели через сеть.')
    try:
        cases = [{'name':'Ответ','task':'Найди пункты о возврате','expected_status':'completed','expected_answer':'Готово'},
                 {'name':'Остановка','task':'Повторяй','expected_status':'budget_limit','expected_answer':''}]
        def run(task):
            if task == 'Повторяй':
                repeat = lambda task, events: {'type':'tool','tool':'read_notes'}
                return run_controlled(task, ROOT/'data'/'notes.txt', repeat, {'steps':3,'tool_calls':2})
            return run_controlled(task, ROOT/'data'/'notes.txt', lambda task, events: {'type':'answer','text':'Готово'}, {'steps':3,'tool_calls':2})
        result = evaluate_cases(cases, run)
    except NotImplementedError as error:
        print(error)
    else:
        print(result)


if __name__ == '__main__':
    main()
