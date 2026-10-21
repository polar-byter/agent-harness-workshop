import unittest
from decisions import parse_decision


class CommandTests(unittest.TestCase):
    def test_json_object_is_returned_without_executing_it(self):
        self.assertEqual(parse_decision('{"type":"tool","tool":"delete_file"}'),
                         {'type': 'tool', 'tool': 'delete_file'})

    def test_answer_uses_the_same_parser(self):
        self.assertEqual(parse_decision('{"type":"answer","text":"Готово"}')['text'], 'Готово')

    def test_wrong_text_and_wrong_json_values_are_rejected(self):
        for text in ('Сейчас поищу', '[]', 'null', '42', '"строка"'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_decision(text)
