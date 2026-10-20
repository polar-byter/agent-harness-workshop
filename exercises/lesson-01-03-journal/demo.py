import json
import hashlib
from pathlib import Path
from notes import find_notes, find_notes_alt, read_notes
from journal import write_result
from app import run_search

ROOT = Path(__file__).resolve().parent


def main():
    print('Учебный запуск без обращения к модели через сеть.')
    try:
        path = ROOT / 'runs.jsonl'
        write_result(path, {'query': 'python', 'matches': ['Python lists']})
        result = path.read_text(encoding='utf-8').splitlines()[-1]
    except NotImplementedError as error:
        print(error)
    else:
        print(result)


if __name__ == '__main__':
    main()
