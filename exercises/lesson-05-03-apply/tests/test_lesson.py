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
        root = ROOT/'scratch'
        path = root/'prices.py'
        path.write_text('old\n', encoding='utf-8')
        proposal = preview_change(root, 'prices.py', 'new\n')
        self.assertFalse(apply_change(root, proposal, False))
        self.assertEqual(path.read_text(encoding='utf-8'), 'old\n')
        self.assertTrue(apply_change(root, proposal, True))
        self.assertEqual(path.read_text(encoding='utf-8'), 'new\n')
        with self.assertRaises(ValueError):
            apply_change(root, proposal, True)


if __name__ == "__main__":
    unittest.main()
