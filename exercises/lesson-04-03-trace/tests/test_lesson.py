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
        path = ROOT/'scratch'/'trace.jsonl'
        path.write_text('old', encoding='utf-8')
        events = [{'command':{'tool':'read_notes'},'result':{'notes':['Заметка']}}]
        save_events(path, events)
        self.assertEqual([json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()], events)
        save_events(path, [])
        self.assertEqual(path.read_text(encoding='utf-8'), '')


if __name__ == "__main__":
    unittest.main()
