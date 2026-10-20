from pathlib import Path
from workspace import workspace_path, prepare_coding_task, apply_change, check_project
from coding_model import propose_live

ROOT = Path(__file__).resolve().parent


def main():
    path = workspace_path(ROOT / 'workspace', 'prices.py')
    print('Разрешённый файл:', path.relative_to(ROOT))
    suggestion = propose_live('Исправь расчёт общей цены', path.read_text(encoding='utf-8'))
    print('Предложение модели, без записи в файл:')
    print(suggestion)


if __name__ == "__main__":
    main()
