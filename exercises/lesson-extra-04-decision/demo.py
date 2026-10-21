"""Настоящий запрос через сохранённое подключение курса."""
from decisions import decide_live
from transport import read_connection


def main():
    settings = read_connection()
    print('Модель:', settings['model'])
    print('Задача: Найди в регламенте пункты о возврате')
    try:
        command = decide_live('Найди в регламенте пункты о возврате', [])
    except (NotImplementedError, ValueError) as error:
        print(error)
    else:
        print(command)


if __name__ == '__main__':
    main()
