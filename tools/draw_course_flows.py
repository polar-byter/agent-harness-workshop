"""Рисуем передачу данных и изменение состояния в учебных примерах."""
import argparse
import math
import runpy
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH = 480
HEIGHT = 650
INK = '#21384c'
MUTED = '#587083'
GREEN = '#147c70'
BLUE = '#315bb0'
PALE = '#e6f3ef'
FONTS = Path('C:/Windows/Fonts')


def font(size=17, bold=False):
    return ImageFont.truetype(str(FONTS / ('segoeuib.ttf' if bold else 'segoeui.ttf')), size)


def paragraph(draw, text, position, width, size=17, color=INK, bold=False):
    """Переносим текст по словам; выход за отведённое место считаем ошибкой."""
    selected = font(size, bold)
    x, y = position
    for source_line in text.split('\n'):
        line = ''
        for word in source_line.split():
            assert draw.textlength(word, font=selected) <= width, word
            candidate = (line + ' ' + word).strip()
            if draw.textlength(candidate, font=selected) > width:
                draw.text((x, y), line, font=selected, fill=color)
                y += size + 6
                line = word
            else:
                line = candidate
        draw.text((x, y), line, font=selected, fill=color)
        y += size + 6
    return y


def panel(draw, box, heading, body, tint='white', size=17):
    left, top, right, bottom = box
    draw.rounded_rectangle(box, radius=12, fill=tint, outline='#cbd8e1', width=1)
    y = paragraph(draw, heading, (left + 14, top + 9), right - left - 28, 16, MUTED, True)
    y = paragraph(draw, body, (left + 14, y + 5), right - left - 28, size)
    assert y <= bottom - 4, (heading, body, y, bottom)


def arrow(draw, points, color=GREEN, width=3):
    draw.line(points, fill=color, width=width, joint='curve')
    x, y = points[-1]
    previous = points[-2]
    angle = math.atan2(y - previous[1], x - previous[0])
    draw.polygon([(x, y), (x - 10 * math.cos(angle - .5), y - 10 * math.sin(angle - .5)),
                  (x - 10 * math.cos(angle + .5), y - 10 * math.sin(angle + .5))], fill=color)


def point_on_route(points, fraction):
    lengths = [math.dist(a, b) for a, b in zip(points, points[1:])]
    remaining = sum(lengths) * fraction
    for a, b, length in zip(points, points[1:], lengths):
        if remaining <= length:
            ratio = remaining / length if length else 0
            return a[0] + ratio * (b[0] - a[0]), a[1] + ratio * (b[1] - a[1])
        remaining -= length
    return points[-1]


def packet(draw, points, fraction, label):
    x, y = point_on_route(points, fraction)
    if fraction >= 1:
        draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=GREEN)
        return
    selected = font(14, True)
    width = draw.textlength(label, font=selected) + 20
    left = max(6, min(WIDTH - width - 6, x - width / 2))
    draw.rounded_rectangle((left, y - 14, left + width, y + 15), 7, fill=BLUE)
    draw.text((left + 10, y - 11), label, font=selected, fill='white')


def base(title, subtitle):
    picture = Image.new('RGB', (WIDTH, HEIGHT), '#f3f7fa')
    draw = ImageDraw.Draw(picture)
    y = paragraph(draw, title, (20, 12), 440, 23, INK, True)
    assert y <= 77, title
    paragraph(draw, subtitle, (20, 80), 440, 14, MUTED)
    draw.line((20, 109, 460, 109), fill='#ccd8e1')
    return picture, draw


def draw_transfer(story, index, progress):
    scene = story['scenes'][index]
    picture, draw = base(story['title'], 'Учебный пример. Значения выбраны для объяснения.')
    paragraph(draw, f'{index + 1}/{len(story["scenes"])}. ' + scene['action'], (20, 120), 440, 19, INK, True)
    panel(draw, (20, 185, 460, 330), scene['source'], scene['before'])
    route = [(240, 331), (240, 395)]
    arrow(draw, route)
    packet(draw, route, progress, scene['packet'])
    arrived = progress >= 1
    panel(draw, (20, 397, 460, 552), scene['destination'],
          scene['after'] if arrived else scene.get('waiting', 'Данные ещё не переданы.'), PALE if arrived else 'white')
    y = paragraph(draw, scene['explanation'], (24, 568), 432, 16, MUTED)
    assert y <= 642, scene['explanation']
    return picture


def draw_summary(story):
    """Статичная версия показывает весь ход, а не последний кадр анимации."""
    picture, draw = base(story['title'], 'Краткая схема того же учебного примера.')
    scenes = story['scenes']
    top = 122
    row_height = min(116, 490 // len(scenes))
    for index, scene in enumerate(scenes):
        draw.ellipse((20, top + 5, 45, top + 30), fill=GREEN)
        draw.text((27, top + 6), str(index + 1), font=font(15, True), fill='white')
        y = paragraph(draw, scene['action'], (57, top), 400, 17, INK, True)
        y = paragraph(draw, scene.get('summary', scene['after']), (57, y + 1), 400, 16, MUTED)
        assert y <= top + row_height, (story['title'], scene['action'], 'summary overflow')
        top += row_height
    return picture


LOOP_STEPS = [
    ('Первый запрос к модели', 'task = "Найди заметки о Python"\nevents = []',
     'Пока результатов нет. Передаём задачу и пустую историю.', [(240, 115), (240, 151)], 'задача + []'),
    ('Модель запросила поиск', 'command = {"type": "tool",\n  "tool": "find_notes", "query": "python"}',
     'Это описание действия. Модель сама файл не открывает.', [(157, 181), (110, 181), (110, 266)], 'find_notes: python'),
    ('Программа разрешила действие', 'dispatch_tool(command, notes_path)\nИмя: "find_notes". Запрос: "python".',
     'Проверяем имя и вызываем поиск в заданном файле.', [(194, 296), (286, 296)], 'query: python'),
    ('Поиск вернул строки', 'result = {"matches": [\n  "Python functions return values.",\n  "Python lists keep item order."]}',
     'Результат возвращается программе, а не напрямую модели.', [(370, 327), (370, 355), (240, 355)], '2 строки'),
    ('Сохраняем событие', 'events.append({\n  "command": command, "result": result\n})\nТеперь в истории одно событие.',
     'В одной записи связываем запрос поиска и найденные строки.', [(240, 355), (240, 386)], 'command + result'),
    ('Второй запрос к модели', 'decide(task, events)\nТа же задача + команда поиска\n+ обе найденные строки.',
     'Возвращаемся к модели. Теперь она получает результат поиска.', [(156, 414), (12, 414), (12, 181), (156, 181)], 'задача + 1 событие'),
    ('Модель вернула итоговый ответ', '{"type": "answer",\n "text": "Найдены две заметки о Python."}',
     'run_agent возвращает completed. Нового поиска в этом примере нет.', [(324, 181), (468, 181), (468, 414), (324, 414)], 'итоговый ответ'),
]


def draw_cycle(index, progress):
    title, data, explanation, route, label = LOOP_STEPS[index]
    picture, draw = base('Как замыкается агентный цикл', 'Пример пути из двух обращений к модели, не запись запуска.')
    actors = [((156, 151, 324, 212), 'Модель', 'выбирает действие'),
              ((26, 266, 194, 327), 'dispatch_tool', 'проверяет и вызывает'),
              ((286, 266, 454, 327), 'find_notes', 'ищет строки'),
              ((156, 386, 324, 447), 'run_agent', 'хранит список events')]
    arrow(draw, [(157, 181), (110, 181), (110, 266)], '#a7b8c4', 2)
    arrow(draw, [(194, 296), (286, 296)], '#a7b8c4', 2)
    arrow(draw, [(370, 327), (370, 355), (240, 355), (240, 386)], '#a7b8c4', 2)
    arrow(draw, [(156, 414), (12, 414), (12, 181), (156, 181)], '#a7b8c4', 2)
    for box, heading, detail in actors:
        panel(draw, box, heading, detail, size=12)
    draw.text((68, 225), '1. Команда', font=font(14), fill=MUTED)
    draw.text((283, 350), '2. Результат', font=font(14), fill=MUTED)
    draw.text((49, 358), '3. В новый', font=font(13), fill=MUTED)
    draw.text((49, 375), 'запрос', font=font(13), fill=MUTED)
    arrow(draw, route)
    packet(draw, route, progress, label)
    has_event = index > 4 or (index == 4 and progress >= 1)
    draw.text((158, 223), 'events: ' + ('[1 событие]' if has_event else '[]'), font=font(14, True), fill=GREEN)
    draw.text((158, 242), 'Вызов модели: ' + ('1' if index < 5 else '2'), font=font(14), fill=MUTED)
    if index == 6:
        draw.text((340, 223), 'Завершение', font=font(13, True), fill=GREEN)
    y = paragraph(draw, f'{index + 1}/7. {title}', (20, 461), 440, 18, INK, True)
    y = paragraph(draw, data, (25, y + 5), 430, 16)
    y = paragraph(draw, explanation, (25, y + 6), 430, 14, MUTED)
    assert y <= 647, (title, y)
    return picture


def cycle_summary():
    story = {'title': 'Почему это цикл', 'scenes': [
        {'action': 'Передаём задачу модели', 'after': 'task + events=[] -> команда find_notes'},
        {'action': 'Программа выполняет поиск', 'after': 'dispatch_tool -> find_notes -> две строки'},
        {'action': 'Сохраняем команду и результат', 'after': 'events.append({command, result})'},
        {'action': 'Снова обращаемся к модели', 'after': 'Та же задача + история с найденными строками'},
        {'action': 'Получаем ответ или повторяем обмен', 'after': 'type="answer" завершает работу; max_steps ограничивает число обращений.'},
    ]}
    picture = draw_summary(story)
    draw = ImageDraw.Draw(picture)
    arrow(draw, [(47, 453), (10, 453), (10, 137), (19, 137)], BLUE, 2)
    return picture


def save_animation(destination, frames, durations):
    destination.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(destination, save_all=True, append_images=frames[1:], duration=durations,
                   loop=0, disposal=2, optimize=True)


def render(story, vault, review_folder):
    destination = vault / story['path']
    frames, durations, keyframes = [], [], []
    cycle = story.get('kind') == 'cycle'
    count = len(LOOP_STEPS) if cycle else len(story['scenes'])
    for index in range(count):
        for tick in range(10):
            progress = tick / 9
            frame = draw_cycle(index, progress) if cycle else draw_transfer(story, index, progress)
            frames.append(frame)
            durations.append(3000 if tick == 9 else (600 if tick == 0 else 70))
        keyframes.append(frames[-1])
    save_animation(destination, frames, durations)
    (cycle_summary() if cycle else draw_summary(story)).save(destination.with_suffix('.png'))
    if review_folder:
        review_folder.mkdir(parents=True, exist_ok=True)
        sheet = Image.new('RGB', (WIDTH * 3, HEIGHT * math.ceil(count / 3)), 'white')
        for index, frame in enumerate(keyframes):
            sheet.paste(frame, ((index % 3) * WIDTH, (index // 3) * HEIGHT))
        sheet.save(review_folder / (destination.stem + '.png'))
    print(destination.name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', type=Path, required=True)
    parser.add_argument('--only', help='Часть имени файла для одного рисунка')
    parser.add_argument('--review-folder', type=Path)
    args = parser.parse_args()
    stories = runpy.run_path(str(Path(__file__).with_name('course_flow_examples.py')))['STORIES']
    for story in stories:
        if not args.only or args.only in story['path']:
            render(story, args.vault, args.review_folder)


if __name__ == '__main__':
    main()
