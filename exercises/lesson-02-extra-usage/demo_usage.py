from model_stats import format_usage
from usage_client import request_sample


def main():
    question = 'Сколько дней есть на возврат товара?'
    notes = ['Возврат товара возможен в течение 14 дней.']
    try:
        # Проверяем готовность функции до обращения к модели.
        format_usage({'input_tokens': 10, 'output_tokens': 0, 'cached_tokens': None})
        answer, stats = request_sample(question, notes)
        print('Ответ модели:', answer)
        for line in format_usage(stats):
            print(line)
        print(f'Время обращения: {stats["elapsed_seconds"]:.2f} с')
        if stats['requested_context_tokens'] is not None:
            print('Запрошенный num_ctx:', stats['requested_context_tokens'])
        speed = stats['output_tokens_per_second']
        if speed is not None:
            print(f'Генерация по данным Ollama: {speed:.1f} токена/с')
    except (NotImplementedError, ValueError) as error:
        print(error)


if __name__ == '__main__':
    main()
