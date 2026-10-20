from pathlib import Path
from workspace import workspace_path, prepare_coding_task, apply_change, check_project
from coding_model import propose_live

ROOT = Path(__file__).resolve().parent


def main():
    proposal = prepare_coding_task('Исправь расчёт общей цены', ROOT / 'workspace', propose_live)
    print(proposal['diff'] or 'Модель не предложила изменений')

    approved = input('Применить показанное изменение к учебному prices.py? Введите да: ').strip().lower() == 'да'
    applied = apply_change(ROOT / 'workspace', proposal, approved)
    print('Изменение применено:', applied)

    print('Результат проверки проекта:', check_project(ROOT / 'workspace'))


if __name__ == "__main__":
    main()
