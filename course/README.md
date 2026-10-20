# От поиска заметок до собственного учебного агента

Мы будем постепенно передавать программе всё больше работы. Сначала она сможет найти данные. Затем модель получит эти данные для ответа, научится запрашивать инструменты, а наш harness — ограничивать действия и сохранять историю. В конце предложим агенту небольшое изменение кода и проверим его результат.

Каждый урок ниже имеет собственный архив. Предыдущие части в нём подготовлены для старта, в функциях текущего задания подготовлено начало, а недописанный участок отмечен `NotImplementedError`. Можно продолжать свой проект или открыть соответствующий каркас в новом окне PyCharm. Первый путь сохраняет вашу реализацию, второй позволяет отдельно пройти конкретный урок.

Начните с [открытия первого проекта](01-note-search/00-setup.md). Если нужно разобраться с окнами редактора, есть [схема поиска файла и запуска](pycharm.md).

## Поиск по заметкам

| Урок | Отдельный каркас |
|---|---|
| [Поисковая функция](01-note-search/01-search.md) | [lesson-01-01-search](../downloads/lesson-01-01-search.zip?raw=true) |
| [Читаем заметки](01-note-search/02-read.md) | [lesson-01-02-read](../downloads/lesson-01-02-read.zip?raw=true) |
| [Сохраняем результат поиска](01-note-search/03-journal.md) | [lesson-01-03-journal](../downloads/lesson-01-03-journal.zip?raw=true) |
| [Соединяем чтение, поиск и журнал](01-note-search/04-run.md) | [lesson-01-04-run](../downloads/lesson-01-04-run.zip?raw=true) |

## Ответ по найденным данным

| Урок | Отдельный каркас |
|---|---|
| [Передаём вопрос вместе с заметками](02-note-assistant/01-messages.md) | [lesson-02-01-messages](../downloads/lesson-02-01-messages.zip?raw=true) |
| [Извлекаем текст из ответа сервиса](02-note-assistant/02-response.md) | [lesson-02-02-response](../downloads/lesson-02-02-response.zip?raw=true) |
| [Соединяем запрос и ответ](02-note-assistant/03-answer.md) | [lesson-02-03-answer](../downloads/lesson-02-03-answer.zip?raw=true) |

## Агент выбирает действие

| Урок | Отдельный каркас |
|---|---|
| [Выполняем команду поиска](03-tool-agent/01-tools.md) | [lesson-03-01-tools](../downloads/lesson-03-01-tools.zip?raw=true) |
| [Возвращаем результат модели](03-tool-agent/02-cycle.md) | [lesson-03-02-cycle](../downloads/lesson-03-02-cycle.zip?raw=true) |

## Управление выполнением

| Урок | Отдельный каркас |
|---|---|
| [Ограничиваем число действий](04-run-control/01-budget.md) | [lesson-04-01-budget](../downloads/lesson-04-01-budget.zip?raw=true) |
| [Выбираем историю для следующего шага](04-run-control/02-context.md) | [lesson-04-02-context](../downloads/lesson-04-02-context.zip?raw=true) |
| [Сохраняем историю выполнения](04-run-control/03-trace.md) | [lesson-04-03-trace](../downloads/lesson-04-03-trace.zip?raw=true) |
| [Сравниваем поведение на сценариях](04-run-control/04-evaluation.md) | [lesson-04-04-evaluation](../downloads/lesson-04-04-evaluation.zip?raw=true) |

## Изменение учебного кода

| Урок | Отдельный каркас |
|---|---|
| [Ограничиваем рабочую папку](05-coding-harness/01-paths.md) | [lesson-05-01-paths](../downloads/lesson-05-01-paths.zip?raw=true) |
| [Показываем предлагаемое изменение](05-coding-harness/02-diff.md) | [lesson-05-02-diff](../downloads/lesson-05-02-diff.zip?raw=true) |
| [Применяем согласованное предложение](05-coding-harness/03-apply.md) | [lesson-05-03-apply](../downloads/lesson-05-03-apply.zip?raw=true) |
| [Проверяем изменённый проект](05-coding-harness/04-verify.md) | [lesson-05-04-verify](../downloads/lesson-05-04-verify.zip?raw=true) |

Во втором подпроекте начинаем с подготовленного файла ответа и затем предлагаем отдельный сетевой запуск. В третьем используем простой учебный протокол команд в JSON; это не нативный function calling API. В четвёртом считаем шаги и вызовы, а не стоимость токенов. Пятый подпроект выполняет один проход изменения с явным согласием и тестами; полноценная изоляция исполнения и самостоятельные повторы остаются дальнейшим развитием.
