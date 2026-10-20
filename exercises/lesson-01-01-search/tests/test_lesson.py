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
        for function in (find_notes, find_notes_alt):
            original = ['Python lists', 'Agent tools', 'python functions', 'Python lists']
            self.assertEqual(function(original, ' PYTHON '), ['Python lists', 'python functions', 'Python lists'])
            self.assertEqual(original, ['Python lists', 'Agent tools', 'python functions', 'Python lists'])
            self.assertEqual(function(['Straße'], 'STRASSE'), ['Straße'])
            self.assertEqual(function(['Python'], 'absent'), [])
            with self.assertRaises(ValueError):
                function(['Python'], '   ')


if __name__ == "__main__":
    unittest.main()
