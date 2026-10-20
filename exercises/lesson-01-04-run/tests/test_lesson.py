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
        path = ROOT / 'scratch' / 'combined.jsonl'
        path.write_text('', encoding='utf-8')
        first = run_search(ROOT / 'data' / 'notes.txt', ' Python ', path)
        self.assertEqual(first['status'], 'found')
        self.assertEqual(first['query'], 'Python')
        self.assertEqual(len(first['matches']), 2)
        second = run_search(ROOT / 'data' / 'notes.txt', 'absent', path)
        self.assertEqual(second['status'], 'not_found')
        self.assertEqual([json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()], [first, second])
        with self.assertRaises(FileNotFoundError):
            run_search(ROOT / 'scratch' / 'missing.txt', 'python', path)


if __name__ == "__main__":
    unittest.main()
