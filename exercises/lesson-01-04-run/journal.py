import json
from pathlib import Path


def write_result(path: Path, result: dict) -> None:
    with path.open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(result, ensure_ascii=False) + '\n')
