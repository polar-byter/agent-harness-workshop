from notes import find_notes, find_notes_alt


def main() -> None:
    notes = ['Python lists', 'Agent tools', 'python functions']
    query = ' PYTHON '
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
