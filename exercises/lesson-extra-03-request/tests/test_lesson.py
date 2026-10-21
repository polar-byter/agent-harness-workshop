from io import BytesIO
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from transport import request_json


class RequestTests(unittest.TestCase):
    def test_body_headers_and_json_response(self):
        with patch('transport.urlopen', return_value=BytesIO(b'{"ok": true}')) as opened:
            result = request_json('https://example.invalid/chat', {'text': 'Привет'}, 'учебный-ключ')
        request = opened.call_args.args[0]
        self.assertEqual(request.get_method(), 'POST')
        self.assertEqual(json.loads(request.data.decode('utf-8')), {'text': 'Привет'})
        self.assertEqual(request.get_header('Authorization'), 'Bearer учебный-ключ')
        self.assertEqual(request.get_header('Content-type'), 'application/json')
        self.assertEqual(opened.call_args.kwargs['timeout'], 180)
        self.assertEqual(result, {'ok': True})

    def test_local_request_has_no_authorization_header(self):
        with patch('transport.urlopen', return_value=BytesIO(b'{}')) as opened:
            request_json('http://127.0.0.1:11434/api/chat', {})
        self.assertIsNone(opened.call_args.args[0].get_header('Authorization'))

    def test_network_failure_stays_a_failure(self):
        with patch('transport.urlopen', side_effect=URLError('нет соединения')):
            with self.assertRaisesRegex(ValueError, 'Нет ответа'):
                request_json('https://example.invalid/chat', {})

    def test_http_401_keeps_a_useful_hint(self):
        error = HTTPError('https://example.invalid/chat', 401, 'ошибка', {}, None)
        try:
            with patch('transport.urlopen', side_effect=error):
                with self.assertRaisesRegex(ValueError, 'API-ключ'):
                    request_json('https://example.invalid/chat', {})
        finally:
            error.close()
