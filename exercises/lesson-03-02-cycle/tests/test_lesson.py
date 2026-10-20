import sys
import unittest
import json
import hashlib
from pathlib import Path
from notes import find_notes, find_notes_alt, read_notes
from assistant import build_messages, extract_answer, answer_question
from transport import send_fixture
from agent import dispatch_tool, run_agent, decide_fixture
ROOT = Path(__file__).resolve().parents[1]


class LessonTests(unittest.TestCase):
    def test_contract(self):
        (ROOT / "scratch").mkdir(exist_ok=True)
        calls = []
        def decide(task, events):
            calls.append(len(events))
            return {'type':'tool','tool':'find_notes','query':'python'} if not events else {'type':'answer','text':'Готово'}
        result = run_agent('Найди Python', ROOT/'data'/'notes.txt', decide, 3)
        self.assertEqual(calls, [0, 1])
        self.assertEqual(result['answer'], 'Готово')
        self.assertEqual(len(result['events'][0]['result']['matches']), 2)
        repeat = lambda task, events: {'type':'tool','tool':'read_notes'}
        self.assertEqual(run_agent('Повтор', ROOT/'data'/'notes.txt', repeat, 2)['status'], 'step_limit')


if __name__ == "__main__":
    unittest.main()
