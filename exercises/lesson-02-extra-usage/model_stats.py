def format_usage(stats: dict) -> list[str]:
    lines = []
    for label, key in (
        ('Токены запроса', 'input_tokens'),
        ('Токены ответа', 'output_tokens'),
        ('Токены из кеша', 'cached_tokens'),
    ):
        value = stats.get(key)
        # Если значения нет, покажите "сервис не сообщил". Ноль сохраняйте как ноль.
        raise NotImplementedError('Допишите format_usage по подсказкам урока и TASK.md')
    return lines
