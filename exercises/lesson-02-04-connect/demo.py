from pathlib import Path
from assistant import answer_question
from transport import send_live

ROOT = Path(__file__).resolve().parent


def main():
    question = 'Сколько дней есть на возврат товара?'
    notes = ['Возврат товара возможен в течение 14 дней.']
    print('Вопрос:', question)
    print('Заметки:', notes)
    answer = answer_question(question, notes, send_live)
    print('Ответ модели:', answer)


if __name__ == "__main__":
    main()
