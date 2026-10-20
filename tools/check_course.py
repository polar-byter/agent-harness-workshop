"""Check repository navigation and starter behavior without network requests."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]


def main():
    config=json.loads((ROOT/'tools'/'course-map.json').read_text(encoding='utf-8'))
    files=[path for path in ROOT.rglob('*.md') if not any(part in ('.checks','.git','.venv') for part in path.relative_to(ROOT).parts)]
    links=0
    for path in files:
        text=path.read_text(encoding='utf-8')
        assert not re.search(r'\[\[[\w][^\]\n]*\]\]',text),(path,'Obsidian link remains')
        assert text.count('```')%2==0,path
        for code in re.findall(r'```python\n(.*?)```',text,re.S):
            ast.parse(code,filename=str(path))
        destinations=re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',text)+re.findall(r'<img[^>]+src="([^"]+)"',text)
        for destination in destinations:
            url=urlsplit(destination)
            if url.scheme or url.netloc or not url.path:
                continue
            target=(path.parent/unquote(url.path)).resolve()
            assert target.is_relative_to(ROOT), (path,destination)
            assert target.exists(),(path,destination)
            links+=1
        for width in re.findall(r'<img[^>]+width="(\d+)"',text):
            assert int(width)<=600,(path,width)
    scratch=ROOT/'.checks'
    scratch.mkdir(exist_ok=True)
    assert scratch.resolve().is_relative_to(ROOT)
    python_files=0
    for lesson in config['lessons']:
        exercise=ROOT/'exercises'/lesson['root']
        assert (exercise/'TASK.md').is_file()
        for path in exercise.rglob('*.py'):
            ast.parse(path.read_text(encoding='utf-8'),filename=str(path));python_files+=1
        archive=ROOT/'downloads'/(lesson['root']+'.zip')
        with ZipFile(archive) as package:
            assert package.testzip() is None,archive
            for name in package.namelist():
                relative=Path(*Path(name).parts[1:])
                if name.endswith('/') or not relative.parts:
                    continue
                if relative.as_posix()!='README.md':
                    assert package.read(name)==(exercise/relative).read_bytes(),(archive,relative)
        # The scratch root and every temporary checkout are verified before managed cleanup.
        with tempfile.TemporaryDirectory(prefix=lesson['root']+'-',dir=scratch) as folder:
            copy=Path(folder).resolve()
            assert copy.is_relative_to(scratch.resolve())
            shutil.copytree(exercise,copy,dirs_exist_ok=True)
            result=subprocess.run([sys.executable,'-B','-c','import demo; demo.main()'],cwd=copy,
                env=dict(os.environ,PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1'),
                capture_output=True,text=True,encoding='utf-8',timeout=15)
            assert result.returncode==0,(lesson['root'],result.stdout,result.stderr)
            assert 'Допишите' in result.stdout,(lesson['root'],result.stdout)
        print(lesson['root']+': starter and archive OK')
    print(f'Checked {len(config["documents"])} course pages, {links} local links, {python_files} Python files and {len(config["lessons"])} starters.')
    print('These checks validate course packaging; unfinished learner functions are expected. No model API calls were made.')


if __name__=='__main__':
    main()
