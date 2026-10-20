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
        self.assertTrue(check_budget({'steps':0,'tool_calls':0}, {'steps':2,'tool_calls':1}))
        self.assertFalse(check_budget({'steps':2,'tool_calls':0}, {'steps':2,'tool_calls':1}))
        self.assertFalse(check_budget({'steps':1,'tool_calls':1}, {'steps':2,'tool_calls':1}))
        with self.assertRaises(ValueError):
            check_budget({'steps':True,'tool_calls':0}, {'steps':2,'tool_calls':1})


if __name__ == "__main__":
    unittest.main()
