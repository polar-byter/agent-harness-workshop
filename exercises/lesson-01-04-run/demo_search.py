from notes import find_notes, find_notes_alt


def main() -> None:
    notes = ['Возврат товара возможен в течение 14 дней.', 'Доставка по городу занимает 1 день.', 'ВОЗВРАТ денег производится на карту покупателя.']
    query = ' Возврат '
    for search in (find_notes, find_notes_alt):
        print(search.__name__)
        try:
            matches = search(notes, query)
        except NotImplementedError as error:
            print(error)
        else:
            print(matches)


if __name__ == '__main__':
    main()
