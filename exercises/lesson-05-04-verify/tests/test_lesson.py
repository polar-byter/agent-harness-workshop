import sys
import unittest
import json
import hashlib
from pathlib import Path
from notes import find_notes, find_notes_alt, read_notes
from assistant import build_messages, extract_answer, answer_question
from transport import send_fixture
from agent import dispatch_tool, run_agent, decide_fixture
from workspace import workspace_path, preview_change, apply_change, check_project, prepare_coding_task
from coding_model import propose_fixture
ROOT = Path(__file__).resolve().parents[1]


class LessonTests(unittest.TestCase):
    def test_contract(self):
        (ROOT / "scratch").mkdir(exist_ok=True)
        root = ROOT/'workspace'
        self.assertFalse(check_project(root)['passed'])
        proposal = prepare_coding_task('Исправь расчёт', root, propose_fixture)
        self.assertTrue(apply_change(root, proposal, True))
        result = check_project(root)
        self.assertTrue(result['passed'], result['output'])
        self.assertEqual(result['returncode'], 0)


if __name__ == "__main__":
    unittest.main()
