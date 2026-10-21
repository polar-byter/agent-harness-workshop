"""Проверяем написанный сетевой участок с настоящей моделью."""
from assistant import answer_question
from transport import send_live


def main():
    try:
        answer = answer_question('Что заметки говорят о Python?',
                                 ['Python lists keep item order.'], send_live)
    except (NotImplementedError, ValueError) as error:
        print(error)
    else:
        print(answer)


if __name__ == '__main__':
    main()
