from pathlib import Path
from workspace import prepare_coding_task, apply_change, check_project
from coding_model import propose_fixture, propose_live

ROOT = Path(__file__).resolve().parent
USE_LIVE_MODEL = False
APPROVED = False


def main():
    propose = propose_live if USE_LIVE_MODEL else propose_fixture
    print('Режим API' if USE_LIVE_MODEL else 'Учебное предложение без сети')
    root = ROOT / 'workspace'
    try:
        proposal = prepare_coding_task('Исправь расчёт общей цены', root, propose)
        print(proposal['diff'])
        if not apply_change(root, proposal, APPROVED):
            print('Изменение не применено: APPROVED = False.')
            return
        result = check_project(root)
    except NotImplementedError as error:
        print(error)
    else:
        print(result)


if __name__ == '__main__':
    main()
