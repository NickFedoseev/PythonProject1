from src.widget import get_date


def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список операций по значению ключа 'state'.

    Args:
        operations (list[dict]): Список словарей с данными об операциях.
        state (str): Значение ключа 'state' для фильтрации. По умолчанию 'EXECUTED'.

    Returns:
        list[dict]: Отфильтрованный список операций.
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
