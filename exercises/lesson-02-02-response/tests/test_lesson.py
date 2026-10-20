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
        response = {'status': 'completed', 'output': [
            {'type': 'reasoning'}, {'type': 'message', 'content': [
            {'type': 'output_text', 'text': 'Первая'}, {'type': 'output_text', 'text': 'Вторая'}]}]}
        self.assertEqual(extract_answer(response), 'Первая\nВторая')
        for invalid in ({'status': 'incomplete', 'output': []}, {'status': 'completed', 'output': []}):
            with self.assertRaises(ValueError):
                extract_answer(invalid)


if __name__ == "__main__":
    unittest.main()
