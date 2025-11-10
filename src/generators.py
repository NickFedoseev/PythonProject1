from typing import Iterator


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    """
    Возвращает итератор, выдающий транзакции с заданной валютой.

    Args:
        transactions: Список транзакций (список словарей).
        currency: Код валюты (например, "USD").

    Yields:
        Транзакции с указанной валютой.
    """
    for transaction in transactions:
        # !!! ИСПРАВЛЕНИЕ: Используем .get() для безопасного доступа !!!
        currency_code = transaction.get("operationAmount", {}).get("currency", {}).get("code")
        if currency_code == currency:
            yield transaction


def transaction_descriptions(transactions: list[dict]) -> Iterator[str]:
    """
    Возвращает итератор, выдающий описания транзакций.

    Args:
        transactions: Список транзакций.

    Yields:
        Описание каждой транзакции.
    """
    for transaction in transactions:
        # !!! ИСПРАВЛЕНИЕ: Используем .get() для безопасного доступа !!!
        description = transaction.get("description")
        if description:
            yield description


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генерирует номера карт длиной 16 цифр с ведущими нулями,
    разделённые пробелами по 4 цифры.
    """
    if start > stop:
        raise ValueError("Начальное значение не может быть больше конечного.")

    if start < 0 or stop < 0:
        raise ValueError("Номера карт не могут быть отрицательными.")

    if stop >= 10**16:
        raise ValueError("Числа должны быть меньше 10^16, чтобы уместиться в 16 цифр.")

    for number in range(start, stop + 1):
        # Преобразуем число в строку и дополняем нулями до 16 символов
        card_str = str(number)
        card_str = "0" * (16 - len(card_str)) + card_str

        # Разбиваем строку на блоки по 4 символа и соединяем пробелами
        # i = 0, 4, 8, 12 → срезы: [0:4], [4:8], [8:12], [12:16]
        formatted = " ".join([card_str[i : i + 4] for i in range(0, 16, 4)])

        yield formatted
