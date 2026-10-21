from pathlib import Path
from agent import dispatch_tool
from decisions import decide_live

ROOT = Path(__file__).resolve().parent


def main():
    task = 'Найди в регламенте пункты о возврате. Сначала запроси инструмент find_notes с query возврат.'
    command = decide_live(task, [])
    print('Команда модели:', command)
    if command.get('type') != 'tool':
        raise ValueError('Модель не запросила инструмент. Сравните команду с заданием; не подставляйте её незаметно.')
    result = dispatch_tool(command, ROOT / 'data' / 'notes.txt')
    print('Результат инструмента:', result)


if __name__ == "__main__":
    main()
