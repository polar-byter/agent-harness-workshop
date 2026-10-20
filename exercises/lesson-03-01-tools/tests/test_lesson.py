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
        path = ROOT / 'data' / 'notes.txt'
        self.assertEqual(len(dispatch_tool({'tool':'find_notes','query':'python'}, path)['matches']), 2)
        self.assertEqual(len(dispatch_tool({'tool':'read_notes'}, path)['notes']), 6)
        for command in ({'tool':'delete'}, {'tool':'find_notes','query':5}):
            with self.assertRaises(ValueError):
                dispatch_tool(command, path)


if __name__ == "__main__":
    unittest.main()
