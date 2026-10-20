from pathlib import Path
from agent import run_agent
from decisions import decide_live

ROOT = Path(__file__).resolve().parent


def main():
    result = run_agent('Найди заметки о Python', ROOT / 'data' / 'notes.txt', decide_live)
    for event in result.get('events', []):
        print(event)
    print(result)


if __name__ == "__main__":
    main()
