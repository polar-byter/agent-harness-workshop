import json
import hashlib
from pathlib import Path
from notes import find_notes, find_notes_alt, read_notes
from assistant import build_messages, extract_answer, answer_question
from transport import send_fixture

ROOT = Path(__file__).resolve().parent


def main():
    print('Учебный запуск без обращения к модели через сеть.')
    try:
        result = extract_answer(json.loads((ROOT / 'data' / 'response.json').read_text(encoding='utf-8')))
    except NotImplementedError as error:
        print(error)
    else:
        print(result)


if __name__ == '__main__':
    main()
