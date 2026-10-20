import difflib
import hashlib
import subprocess
import sys
from pathlib import Path


def workspace_path(root: Path, relative: str) -> Path:
    root = root.resolve()
    candidate = (root / relative).resolve()
    raise NotImplementedError("Допишите workspace_path по подсказкам урока")


def preview_change(root: Path, relative: str, new_text: str) -> dict:
    raise NotImplementedError("Допишите preview_change по подсказкам урока")


def apply_change(root: Path, proposal: dict, approved: bool) -> bool:
    raise NotImplementedError("Допишите apply_change по подсказкам урока")


def check_project(root: Path) -> dict:
    raise NotImplementedError("Допишите check_project по подсказкам урока")


def prepare_coding_task(task: str, root: Path, propose) -> dict:
    path = workspace_path(root, 'prices.py')
    new_text = propose(task, path.read_text(encoding='utf-8'))
    if not isinstance(new_text, str):
        raise ValueError('Предложение должно содержать текст Python-файла')
    return preview_change(root, 'prices.py', new_text)
