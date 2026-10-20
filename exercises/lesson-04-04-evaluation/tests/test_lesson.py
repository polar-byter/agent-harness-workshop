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
        cases = [{'name':'Да','task':'a','expected_status':'completed','expected_answer':'ok'},
                 {'name':'Нет','task':'b','expected_status':'completed','expected_answer':'other'}]
        result = evaluate_cases(cases, lambda task: {'status':'completed','answer':'ok'})
        self.assertEqual((result['passed'],result['total']), (1,2))
        self.assertEqual(result['results'], [{'name':'Да','passed':True},{'name':'Нет','passed':False}])
        self.assertEqual(evaluate_cases([], lambda task: None), {'passed':0,'total':0,'results':[]})


if __name__ == "__main__":
    unittest.main()
