from pathlib import Path
from notes import find_notes, read_notes
from journal import write_result


def run_search(notes_path: Path, query: str, journal_path: Path) -> dict:
    notes = read_notes(notes_path)
    matches = find_notes(notes, query)
    raise NotImplementedError("Допишите run_search по подсказкам урока")
