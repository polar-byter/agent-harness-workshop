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
        result = [find_notes(['Python lists', 'Agent tools', 'python functions'], ' PYTHON '), find_notes_alt(['Python lists', 'Agent tools', 'python functions'], ' PYTHON ')]
    except NotImplementedError as error:
        print(error)
    else:
        print(result)


if __name__ == '__main__':
    main()
