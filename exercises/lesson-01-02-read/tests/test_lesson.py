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
    def test_contract(self):
        (ROOT / "scratch").mkdir(exist_ok=True)
        path = ROOT / 'scratch' / 'read.txt'
        path.write_text('  Первая  \n\nВторая\nПервая\n', encoding='utf-8')
        self.assertEqual(read_notes(path), ['Первая', 'Вторая', 'Первая'])
        path.write_text('', encoding='utf-8')
        self.assertEqual(read_notes(path), [])
        with self.assertRaises(FileNotFoundError):
            read_notes(ROOT / 'scratch' / 'absent.txt')


if __name__ == "__main__":
    unittest.main()
