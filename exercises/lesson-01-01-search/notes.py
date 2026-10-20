from pathlib import Path


def find_notes(notes: list[str], query: str) -> list[str]:
    query = query.strip().casefold()
    if not query:
        raise ValueError('Введите непустой запрос')
    selected = []
    raise NotImplementedError("Допишите find_notes по подсказкам урока")


def find_notes_alt(notes: list[str], query: str) -> list[str]:
    query = query.strip().casefold()
    if not query:
        raise ValueError('Введите непустой запрос')
    raise NotImplementedError("Допишите find_notes_alt по подсказкам урока")


def read_notes(path: Path) -> list[str]:
    raise NotImplementedError("Допишите read_notes по подсказкам урока")
