"""Export the reader course, preserving local edits and ordinary GitHub links."""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
from urllib.parse import quote
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def plain_punctuation(text):
    substitutions={'\u2014':'-','\u2013':'-','\u2192':'->','\u2190':'<-','\u2026':'...','\u00b7':'/','\u00a0':' '}
    for old,new in substitutions.items():
        text=text.replace(old,new)
    return text


def relative_link(source, target):
    return quote(os.path.relpath(target, source.parent).replace('\\', '/'), safe='/.-_')


def main():
    parser=argparse.ArgumentParser(description='Экспорт читательских уроков из Obsidian')
    parser.add_argument('--vault',type=Path,required=True,help='Корень хранилища Obsidian')
    args=parser.parse_args()
    vault=args.vault.resolve()
    config=json.loads((ROOT/'tools'/'course-map.json').read_text(encoding='utf-8'))
    previous_path=ROOT/'maintainer'/'export-manifest.json'
    previous=json.loads(previous_path.read_text(encoding='utf-8')) if previous_path.exists() else {'files':{}}
    mapping={item['source']:item['path'] for item in config['documents']}
    assets={}
    archives={}
    for lesson in config['lessons']:
        mapping[lesson['archive_source']]='downloads/'+lesson['root']+'.zip'
        archives[lesson['archive_source']]='downloads/'+lesson['root']+'.zip'
    for item in config['documents']:
        source=vault/item['source']
        text=source.read_text(encoding='utf-8')
        for match in re.finditer(r'!\[\[([^]|]+)(?:\|[^]]*)?\]\]',text):
            target=match.group(1).split('#')[0]
            if target in mapping:
                continue
            group=next((group for group in config['groups'] if '/'+group['source']+'/' in target),None)
            destination='assets/'+(group['path'] if group else 'common')+'/'+Path(target).name
            mapping[target]=destination
            assets[target]=destination
    pending={}

    def stage(relative,data):
        if Path(relative).suffix in ('.md','.py','.json','.txt','.toml') or Path(relative).name=='.gitignore':
            data=data.replace(b'\r\n',b'\n')
        if Path(relative).suffix=='.md':
            data=plain_punctuation(data.decode('utf-8')).encode('utf-8')
        target=ROOT/relative
        if target.exists():
            current=target.read_bytes()
            known=previous['files'].get(relative)
            if current!=data and (known is None or digest(current)!=known):
                raise ValueError('Файл изменён вручную; экспорт его не перезаписал: '+relative)
        pending[relative]=data

    def convert(text,destination):
        text=re.sub(r'\A---\r?\n.*?\r?\n---\r?\n', '',text,count=1,flags=re.S).lstrip()
        def collapse(match):
            label=match.group(1).strip() or 'Статичный вариант'
            inner=re.sub(r'^> ?', '',match.group(2),flags=re.M).strip()
            return '<details>\n<summary>'+html.escape(label)+'</summary>\n\n'+inner+'\n\n</details>\n'
        text=re.sub(r'^> \[!\w+\]-\s*(.*?)\n((?:>.*(?:\n|$))+)',collapse,text,flags=re.M)
        def link(match):
            embedded,raw,label=match.groups()
            source,sep,anchor=raw.partition('#')
            key=source if source in mapping else source+'.md'
            if key not in mapping:
                raise ValueError('Нет читательского назначения для ссылки: '+raw)
            target=mapping[key]
            url=relative_link(Path(destination),Path(target))
            if sep:
                url+='#'+quote(anchor.lower().replace(' ','-'))
            if embedded:
                width=int(label) if label and label.isdigit() else 480
                return f'<img src="{html.escape(url)}" width="{width}" alt="{html.escape(Path(source).stem)}">'
            if target.endswith('.zip'):
                url+='?raw=true'
            return '['+(label or Path(source).stem)+']('+url+')'
        text=re.sub(r'(!?)\[\[([^]|]+)(?:\|([^]]*))?\]\]',link,text)
        return plain_punctuation(text.strip())+'\n'

    lesson_by_source={lesson['source']:lesson for lesson in config['lessons']}
    for document in config['documents']:
        destination=document['path']
        text=convert((vault/document['source']).read_text(encoding='utf-8'),destination)
        lesson=lesson_by_source.get(document['source'])
        if lesson:
            local=Path('exercises')/lesson['root']
            source_url=relative_link(Path(destination),local/'README.md')
            task_url=relative_link(Path(destination),local/'TASK.md')
            text=text.replace('\n\n', '\n\n[Открыть исходники этого урока]('+source_url+') · [Подсказки рядом с кодом]('+task_url+')\n\n',1)
        stage(destination,text.encode('utf-8'))
    for source,destination in assets.items():
        stage(destination,(vault/source).read_bytes())
    for source,destination in archives.items():
        data=(vault/source).read_bytes()
        stage(destination,data)
        lesson=next(lesson for lesson in config['lessons'] if lesson['archive_source']==source)
        with ZipFile(vault/source) as archive:
            assert archive.testzip() is None
            for name in archive.namelist():
                parts=Path(name).parts
                if not parts or parts[0]!=lesson['root'] or '..' in parts:
                    raise ValueError('Недопустимый путь в архиве: '+name)
                relative=Path(*parts[1:])
                if not relative.parts or name.endswith('/'):
                    continue
                target=(Path('exercises')/lesson['root']/relative).as_posix()
                content=archive.read(name)
                if relative.as_posix()=='README.md':
                    lesson_url=relative_link(Path(target),Path(lesson['path']))
                    content=('['+lesson['title']+']('+lesson_url+') · [Оглавление курса](../../course/README.md)\n\n').encode('utf-8')+content
                stage(target,content)
    for relative,data in pending.items():
        target=ROOT/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(data)
    manifest={'format':1,'source':'Obsidian reader course only','documents':len(config['documents']),
        'lessons':len(config['lessons']),'files':{relative:digest(data) for relative,data in sorted(pending.items())}}
    previous_path.parent.mkdir(exist_ok=True)
    previous_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Exported',len(config['documents']),'documents,',len(config['lessons']),'lesson starters,',len(assets),'images')


if __name__=='__main__':
    main()
