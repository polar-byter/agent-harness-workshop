from pathlib import Path
from assistant import build_messages, extract_answer
from local_model import send_local
from local_runtime import load_model

ROOT = Path(__file__).resolve().parent


def main():
    question = 'Сколько дней есть на возврат товара?'
    notes = ['Возврат товара возможен в течение 14 дней.']
    print('Вопрос:', question)
    print('Заметки:', notes)
    try:
        # Проверяем упражнение до загрузки модели и установки библиотеки.
        from demo_check import check_exercise
        check_exercise()
        print('Загружаем модель из файла...')
        with load_model(ROOT / 'models/Qwen3-0.6B-Q8_0.gguf') as model:
            messages = build_messages(question, notes)
            response = send_local(model, messages)
            print('Ответ модели:', extract_answer(response))
    except (NotImplementedError, FileNotFoundError, ModuleNotFoundError, ValueError) as error:
        print(error)


if __name__ == '__main__':
    main()
