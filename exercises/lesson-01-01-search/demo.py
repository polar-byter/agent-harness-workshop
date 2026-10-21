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
        result = [find_notes(['Возврат товара возможен в течение 14 дней.', 'Доставка по городу занимает 1 день.', 'ВОЗВРАТ денег производится на карту покупателя.'], ' Возврат '), find_notes_alt(['Возврат товара возможен в течение 14 дней.', 'Доставка по городу занимает 1 день.', 'ВОЗВРАТ денег производится на карту покупателя.'], ' Возврат ')]
    except NotImplementedError as error:
        print(error)
    else:
        print(result)


if __name__ == '__main__':
    main()
