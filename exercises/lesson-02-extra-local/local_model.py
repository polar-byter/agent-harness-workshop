from local_runtime import prepare_messages, convert_response


def send_local(model, messages: list[dict]) -> dict:
    prepared = prepare_messages(messages)
    # Передаём сообщения загруженной модели и возвращаем ответ в формате курса.
    raise NotImplementedError('Допишите send_local по подсказкам урока')
