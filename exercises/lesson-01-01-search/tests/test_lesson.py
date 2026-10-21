import sys
import unittest
import json
import hashlib
from pathlib import Path
from notes import find_notes, find_notes_alt, read_notes
from journal import write_result
from app import run_search
ROOT = Path(__file__).resolve().parents[1]


class LessonTests(unittest.TestCase):
    def test_find_notes(self):
        self.check_search(find_notes)

    def test_find_notes_alt(self):
        # Запись в одну строку - необязательная часть урока.
        try:
            find_notes_alt(['Возврат товара'], 'возврат')
        except NotImplementedError:
            self.skipTest('find_notes_alt ещё не дописана: это необязательное задание')
        self.check_search(find_notes_alt)

    def check_search(self, function):
        original = ['Возврат товара возможен в течение 14 дней.', 'Доставка по городу занимает 1 день.', 'ВОЗВРАТ денег производится на карту покупателя.', 'Возврат товара возможен в течение 14 дней.']
        self.assertEqual(function(original, ' Возврат '), ['Возврат товара возможен в течение 14 дней.', 'ВОЗВРАТ денег производится на карту покупателя.', 'Возврат товара возможен в течение 14 дней.'])
        self.assertEqual(original, ['Возврат товара возможен в течение 14 дней.', 'Доставка по городу занимает 1 день.', 'ВОЗВРАТ денег производится на карту покупателя.', 'Возврат товара возможен в течение 14 дней.'])
        self.assertEqual(function(['Straße'], 'STRASSE'), ['Straße'])
        self.assertEqual(function(['Возврат товара'], 'обмен'), [])
        with self.assertRaises(ValueError):
            function(['Возврат товара'], '   ')


if __name__ == "__main__":
    unittest.main()
