from assistant import build_messages, extract_answer
from local_model import send_local


class ExampleModel:
    def __init__(self):
        self.calls = []

    def create_chat_completion(self, **settings):
        self.calls.append(settings)
        return {'choices': [{'finish_reason': 'stop', 'message': {
            'content': 'Списки Python сохраняют порядок элементов.'
        }}]}


def check_exercise():
    model = ExampleModel()
    messages = build_messages('Что заметки говорят о Python?', ['Python lists keep item order.'])
    response = send_local(model, messages)
    assert len(model.calls) == 1, 'Ожидаем один вызов модели'
    settings = model.calls[0]
    assert settings['messages'][0]['role'] == 'system', 'Передайте prepared'
    assert settings['max_tokens'] == 256, 'Сохраните лимит из урока'
    assert messages[0]['role'] == 'developer', 'Исходные сообщения не изменяем'
    assert extract_answer(response) == 'Списки Python сохраняют порядок элементов.'
    return extract_answer(response)


def main():
    try:
        print('Проверка без модели:', check_exercise())
    except NotImplementedError as error:
        print(error)


if __name__ == '__main__':
    main()
