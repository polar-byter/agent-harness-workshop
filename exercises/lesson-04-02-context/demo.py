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
        result = select_context('Найди Python', [{'step':1},{'step':2},{'step':3}], 2)
    except NotImplementedError as error:
        print(error)
    else:
        print(result)


if __name__ == '__main__':
    main()
