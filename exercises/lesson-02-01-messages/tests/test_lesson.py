import sys
import unittest
import json
import hashlib
from pathlib import Path
from notes import find_notes, find_notes_alt, read_notes
from assistant import build_messages, extract_answer, answer_question
from transport import send_fixture
ROOT = Path(__file__).resolve().parents[1]


class LessonTests(unittest.TestCase):
    def test_contract(self):
        (ROOT / "scratch").mkdir(exist_ok=True)
        messages = build_messages('Вопрос', ['Исходная заметка'])
        self.assertEqual([m['role'] for m in messages], ['developer', 'user'])
        data = json.loads(messages[1]['content'])
        self.assertEqual(data, {'question': 'Вопрос', 'notes': ['Исходная заметка']})
        self.assertTrue(messages[0]['content'].strip())
        with self.assertRaises(ValueError):
            build_messages('  ', [])


if __name__ == "__main__":
    unittest.main()
