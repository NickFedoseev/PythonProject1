def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список операций по значению ключа 'state'.

    Args:
        operations (list[dict]): Список словарей с данными об операциях.
        state (str): Значение ключа 'state' для фильтрации. По умолчанию 'EXECUTED'.

    Returns:
        list[dict]: Отфильтрованный список операций.
    """
    return [op for op in operations if op.get("state") == state]


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует список операций по дате.

    Args:
        operations (list[dict]): Список словарей с данными об операциях.
        reverse (bool): Порядок сортировки: по убыванию (True), по возрастанию (False).

    Returns:
        list[dict]: Список операций, отсортированный по дате.
    """
    return sorted(operations, key=lambda x: x["date"], reverse=reverse)


if __name__ == "__main__":
    from pprint import pprint

    data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}
    ]

    print("Отфильтровать по EXECUTED:")
    pprint(filter_by_state(data))

    print("\nОтфильтровать по CANCELED:")
    pprint(filter_by_state(data, "CANCELED"))

    print("\nСортировка по дате (по убыванию):")
    pprint(sort_by_date(data))

    print("\nСортировка по дате (по возрастанию):")
    pprint(sort_by_date(data, reverse=False))
