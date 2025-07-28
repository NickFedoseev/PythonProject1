from src.widget import get_date


def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует операции по статусу.

    Args:
        operations: Список операций (каждая — словарь с ключом 'state').
        state: Статус для фильтрации. По умолчанию — 'EXECUTED'.

    Returns:
        Список операций с указанным статусом.
    """
    return [
        operation
        for operation in operations
        if operation.get("state") == state
    ]


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует операции по дате.

    Args:
        operations: Список операций (каждая — словарь с ключом 'date').
        reverse: Если True, сортирует от новых к старым.

    Returns:
        Отсортированный список операций.
    """
<<<<<<< HEAD
    try:
        return sorted(
            operations,
            key=lambda x: tuple(int(part) for part in reversed(get_date(x['date']).split('.'))),
            reverse=reverse
        )
    except ValueError as e:
        raise ValueError(f"Неверный формат даты: {str(e)}")
    except KeyError:
        raise KeyError("Отсутствует ключ 'date'")
=======
    return sorted(
        operations,
        key=lambda operation: operation["date"],
        reverse=reverse
    )


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
>>>>>>> develop
