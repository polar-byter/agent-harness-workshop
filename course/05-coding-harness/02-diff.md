# Урок 2. Показываем предлагаемое изменение (Генерация Unified Diff)

[Открыть исходники этого урока](../../exercises/lesson-05-02-diff/README.md) / [Подсказки рядом с кодом](../../exercises/lesson-05-02-diff/TASK.md)

> **Где мы находимся:** Кодирующий ассистент нашел ошибку в коде и подготовил исправление. 
> 
> Но надежная программа никогда не перезаписывает файл вслепую!
> 
> Сначала она генерирует наглядный отчет об изменениях - **Unified Diff** (ровно такой же, как вы видите на GitHub в Pull Request), показывая красным удаленные строки и зеленым добавленные:
> 
> `Старый файл + Новый файл -> [difflib.unified_diff] -> наглядный патч (diff)`

---

## Как устроен Diff в стандартной библиотеке Python?

В Python есть встроенный модуль `difflib`:
```python
import difflib

def make_diff(old_text: str, new_text: str, filename: str) -> str:
    lines = difflib.unified_diff(
        old_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile=filename,
        tofile=filename,
    )
    return ''.join(lines)
```

Разработчик своими глазами видит каждую измененную строчку до того, как файл на диске будет тронут!

-> [Урок 3. Применяем согласованное предложение](03-apply.md)
