import sys


def main():
    print('Python:', sys.version.split()[0])
    print('Интерпретатор:', sys.executable)
    try:
        import llama_cpp
    except (ImportError, OSError) as error:
        print('Библиотека пока не загрузилась:', error)
        return
    print('Библиотека загружена:', llama_cpp.__version__)


if __name__ == '__main__':
    main()
