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
        calls = []
        def fake_send(messages):
            calls.append(messages)
            return {'status':'completed', 'output':[{'type':'message','content':[{'type':'output_text','text':'Ответ'}]}]}
        self.assertEqual(answer_question('Вопрос', ['Заметка'], fake_send), 'Ответ')
        self.assertEqual(calls[0], build_messages('Вопрос', ['Заметка']))
        self.assertEqual(len(calls), 1)
        self.assertEqual(answer_question('Вопрос', [], fake_send), 'Подходящих заметок нет.')
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()
