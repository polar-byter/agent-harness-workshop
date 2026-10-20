import sys
import unittest
import json
import hashlib
from pathlib import Path
from notes import find_notes, find_notes_alt, read_notes
from assistant import build_messages, extract_answer, answer_question
from transport import send_fixture
from agent import dispatch_tool, run_agent, decide_fixture
from control import check_budget, select_context, save_events, evaluate_cases, run_controlled
ROOT = Path(__file__).resolve().parents[1]


class LessonTests(unittest.TestCase):
    def test_contract(self):
        (ROOT / "scratch").mkdir(exist_ok=True)
        events = [{'step':1},{'step':2},{'step':3}]
        self.assertEqual(select_context('Задача', events, 2), {'task':'Задача','events':[{'step':2},{'step':3}]})
        self.assertEqual(select_context('Задача', events, 0)['events'], [])
        self.assertEqual(len(events), 3)
        with self.assertRaises(ValueError):
            select_context('Задача', events, -1)


if __name__ == "__main__":
    unittest.main()
