import json
import hashlib
from pathlib import Path
from notes import find_notes, find_notes_alt, read_notes
from assistant import build_messages, extract_answer, answer_question
from transport import send_fixture
from agent import dispatch_tool, run_agent, decide_fixture
from workspace import workspace_path, preview_change, apply_change, check_project, prepare_coding_task
from coding_model import propose_fixture

ROOT = Path(__file__).resolve().parent


def main():
    print('Учебный запуск без обращения к модели через сеть.')
    try:
        proposal = prepare_coding_task('Исправь расчёт общей цены', ROOT/'workspace', propose_fixture)
        print(proposal['diff'])
        approved = False
        result = apply_change(ROOT/'workspace', proposal, approved)
    except NotImplementedError as error:
        print(error)
    else:
        print(result)


if __name__ == '__main__':
    main()
