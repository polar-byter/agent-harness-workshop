from pathlib import Path


def find_notes(notes: list[str], query: str) -> list[str]:
    query = query.strip().casefold()
    if not query:
        raise ValueError('Введите непустой запрос')
    matches = []
    for note in notes:
        if query in note.casefold():
            matches.append(note)
    return matches


def find_notes_alt(notes: list[str], query: str) -> list[str]:
    query = query.strip().casefold()
    if not query:
        raise ValueError('Введите непустой запрос')
    return [note for note in notes if query in note.casefold()]


def read_notes(path: Path) -> list[str]:
    notes = []
    for line in path.read_text(encoding='utf-8').splitlines():
        cleaned = line.strip()
        if cleaned:
            notes.append(cleaned)
    return notes
