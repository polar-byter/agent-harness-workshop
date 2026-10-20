"""Contract checks for adapters; no external model requests."""
from io import BytesIO
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

sys.path.insert(0, str(Path(__file__).resolve().parent / 'model_runtime'))
import transport


class ModelTransportTests(unittest.TestCase):
    messages = [{'role': 'developer', 'content': 'Правила'}, {'role': 'user', 'content': 'Вопрос'}]

    def request(self, provider, response):
        settings = {'provider': provider, 'model': 'test-model', 'api_key': 'local-test-key'}
        stream = BytesIO(json.dumps(response).encode('utf-8'))
        with patch.object(transport, 'read_connection', return_value=settings), \
             patch.object(transport, 'urlopen', return_value=stream) as open_request:
            result = transport.send_live(self.messages)
        request = open_request.call_args.args[0]
        return result, request, json.loads(request.data)

    def test_cloud_payloads_and_common_response(self):
        for provider, url in [('openrouter', 'https://openrouter.ai/api/v1/chat/completions'),
                              ('vsegpt', 'https://api.vsegpt.ru/v1/chat/completions')]:
            with self.subTest(provider=provider):
                result, request, payload = self.request(provider, {
                    'choices': [{'finish_reason': 'stop', 'message': {'content': 'Ответ'}}]})
                self.assertEqual(request.full_url, url)
                self.assertEqual(request.get_header('Authorization'), 'Bearer local-test-key')
                self.assertEqual(payload['messages'][0]['role'], 'system')
                self.assertEqual(payload['messages'][1], self.messages[1])
                self.assertEqual(result, transport.course_response('Ответ'))
        self.assertEqual(self.messages[0]['role'], 'developer')

    def test_local_cpu_request_without_cloud_credentials(self):
        result, request, payload = self.request('ollama', {
            'done': True, 'done_reason': 'stop', 'message': {'content': 'Локальный ответ'}})
        self.assertEqual(request.full_url, 'http://127.0.0.1:11434/api/chat')
        self.assertIsNone(request.get_header('Authorization'))
        self.assertEqual(payload['options']['num_gpu'], 0)
        self.assertIs(payload['think'], False)
        self.assertIs(payload['stream'], False)
        self.assertEqual(result, transport.course_response('Локальный ответ'))

    def test_reject_incomplete_and_missing_text(self):
        cases = [('openrouter', {'choices': []}),
                 ('openrouter', {'choices': [{'finish_reason': 'length', 'message': {'content': 'Часть'}}]}),
                 ('vsegpt', {'choices': [{'finish_reason': 'stop', 'message': {'content': ''}}]}),
                 ('ollama', {'done': False, 'message': {'content': 'Часть'}}),
                 ('ollama', {'done': True, 'done_reason': 'length', 'message': {'content': 'Часть'}})]
        for provider, response in cases:
            with self.subTest(provider=provider, response=response), self.assertRaises(ValueError):
                self.request(provider, response)

    def test_reject_dictionary_instead_of_message_list(self):
        with self.assertRaisesRegex(ValueError, 'список сообщений'):
            transport.send_live({'messages': self.messages})

    def test_connection_errors_do_not_fall_back_to_fixture(self):
        for error in (HTTPError('https://example.invalid', 401, '', {}, None),
                      HTTPError('https://example.invalid', 429, '', {}, None), URLError('offline')):
            with self.subTest(error=type(error)), patch.object(transport, 'urlopen', side_effect=error), \
                 self.assertRaises(ValueError):
                transport.request_json('https://example.invalid', {})


if __name__ == '__main__':
    unittest.main()
