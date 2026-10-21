"""Настоящий запрос через сохранённое подключение курса."""
from decisions import decide_live
from transport import read_connection


def main():
    settings = read_connection()
    print('Модель:', settings['model'])
    print('Задача: Найди заметки о Python')
    try:
        command = decide_live('Найди заметки о Python', [])
    except (NotImplementedError, ValueError) as error:
        print(error)
    else:
        print(command)


if __name__ == '__main__':
    main()
