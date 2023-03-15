BOOK_PATH = 'book/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


# Функция, возвращающая строку с текстом страницы и её размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    i_max = 0
    for symbol in ',.!:;?':
        symbol_number = text.rfind(symbol, start, start + size)
        if len(text) - 1 > symbol_number and text[symbol_number + 1] == '.':
            end = text.rfind(' ', start, start + size)
            symbol_number = text.rfind(symbol, start, end)
        i_max = symbol_number if i_max < symbol_number else i_max
    page_text = text[start:i_max + 1]
    return page_text, len(page_text)


# Функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    with open(path) as b:
        book_file = b.read()

    book_len = len(book_file)
    start = 0
    page = 1
    while start < book_len:
        page_text, page_len = _get_part_text(book_file, start, size=PAGE_SIZE)
        book[page] = page_text.lstrip()
        start += page_len
        page += 1


# Вызов функции prepare_book для подготовки книги из словаря
prepare_book(BOOK_PATH)
