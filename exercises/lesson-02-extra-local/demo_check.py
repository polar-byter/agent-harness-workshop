from assistant import build_messages, extract_answer
from local_model import send_local


class ExampleModel:
    def __init__(self):
        self.calls = []

    def create_chat_completion(self, **settings):
        self.calls.append(settings)
        return {'choices': [{'finish_reason': 'stop', 'message': {
            'content': 'Вернуть товар можно в течение 14 дней.'
        }}]}


def check_exercise():
    model = ExampleModel()
    messages = build_messages('Сколько дней есть на возврат товара?', ['Возврат товара возможен в течение 14 дней.'])
    response = send_local(model, messages)
    assert len(model.calls) == 1, 'Ожидаем один вызов модели'
    settings = model.calls[0]
    assert settings['messages'][0]['role'] == 'system', 'Передайте prepared'
    assert settings['max_tokens'] == 256, 'Сохраните лимит из урока'
    assert messages[0]['role'] == 'developer', 'Исходные сообщения не изменяем'
    assert extract_answer(response) == 'Вернуть товар можно в течение 14 дней.'
    return extract_answer(response)


def main():
    try:
        print('Проверка без модели:', check_exercise())
    except NotImplementedError as error:
        print(error)


if __name__ == '__main__':
    main()
