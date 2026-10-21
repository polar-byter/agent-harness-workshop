import json
import unittest
from decisions import build_decision_messages, RULES


class MessagesTests(unittest.TestCase):
    def test_task_and_events_keep_their_values(self):
        events = [{'tool': 'find_notes', 'result': ['Python lists keep item order.']}]
        messages = build_decision_messages('Найди заметки о Python', events)
        self.assertEqual(messages[0], {'role': 'developer', 'content': RULES})
        self.assertEqual(messages[1]['role'], 'user')
        self.assertEqual(json.loads(messages[1]['content']),
                         {'task': 'Найди заметки о Python', 'events': events})
        self.assertIn('Найди', messages[1]['content'])
        self.assertEqual(events[0]['result'], ['Python lists keep item order.'])

    def test_initial_history_can_be_empty(self):
        self.assertEqual(json.loads(build_decision_messages('Задача', [])[1]['content'])['events'], [])
