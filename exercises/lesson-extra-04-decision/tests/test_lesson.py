import json
import unittest
from unittest.mock import patch
from decisions import decide_live
from transport import course_response


class DecisionTests(unittest.TestCase):
    def test_task_and_history_reach_the_model(self):
        events = [{'tool': 'find_notes', 'result': ['Python lists keep item order.']}]
        with patch('decisions.send_live', return_value=course_response('{"type":"answer","text":"Готово"}')) as send:
            result = decide_live('Найди заметки о Python', events)
        messages = send.call_args.args[0]
        self.assertEqual(json.loads(messages[1]['content'])['events'], events)
        self.assertEqual(json.loads(messages[1]['content'])['task'], 'Найди заметки о Python')
        self.assertEqual(result, {'type': 'answer', 'text': 'Готово'})
        send.assert_called_once()

    def test_non_json_answer_is_rejected(self):
        with patch('decisions.send_live', return_value=course_response('Сейчас поищу')):
            with self.assertRaises(ValueError):
                decide_live('Найди заметки о Python', [])

    def test_incomplete_response_is_not_parsed(self):
        with patch('decisions.send_live', return_value={'status': 'incomplete', 'output': []}):
            with self.assertRaisesRegex(ValueError, 'не завершён'):
                decide_live('Найди заметки о Python', [])
