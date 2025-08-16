import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_operations() -> list[dict]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-01T12:00:00"},
        {"id": 2, "state": "PENDING", "date": "2023-10-02T12:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-10-03T12:00:00"},
        {"id": 4, "state": "CANCELED", "date": "2023-10-04T12:00:00"},
        {"id": 5, "state": "EXECUTED", "date": "2023-10-05T12:00:00"},
        {"id": 6, "date": "2023-10-06T12:00:00"},  # Нет ключа 'state'
    ]


@pytest.fixture
def operations_with_same_date() -> list[dict]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-01T12:00:00"},
        {"id": 2, "state": "EXECUTED", "date": "2023-10-01T12:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-10-01T12:00:00"},
    ]


@pytest.fixture
def operations_with_invalid_dates() -> list[dict]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-01T12:00:00"},
        {"id": 2, "state": "EXECUTED", "date": "invalid_date"},
        {"id": 3, "state": "EXECUTED", "date": "2023-10-03T12:00:00"},
    ]


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3, 5]),
        ("PENDING", [2]),
        ("CANCELED", [4]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state(sample_operations: list[dict], state: str, expected_ids: list[int]) -> None:
    """Тестирование фильтрации операций по статусу."""
    filtered = filter_by_state(sample_operations, state)
    assert [op["id"] for op in filtered] == expected_ids


def test_filter_by_state_empty_list() -> None:
    """Тестирование фильтрации пустого списка операций."""
    assert filter_by_state([]) == []


def test_filter_by_state_default(sample_operations: list[dict]) -> None:
    """Тестирование фильтрации с параметром state по умолчанию."""
    filtered = filter_by_state(sample_operations)
    assert [op["id"] for op in filtered] == [1, 3, 5]


@pytest.mark.parametrize(
    "reverse, expected_ids",
    [
        (True, [6, 5, 4, 3, 2, 1]),
        (False, [1, 2, 3, 4, 5, 6]),
    ],
)
def test_sort_by_date(sample_operations: list[dict], reverse: bool, expected_ids: list[int]) -> None:
    """Тестирование сортировки операций по дате."""
    sorted_ops = sort_by_date(sample_operations, reverse=reverse)
    assert [op["id"] for op in sorted_ops] == expected_ids


def test_sort_by_date_with_same_date(operations_with_same_date: list[dict]) -> None:
    """Тестирование сортировки операций с одинаковыми датами."""
    sorted_ops = sort_by_date(operations_with_same_date)
    # Порядок элементов с одинаковой датой должен сохраниться
    assert [op["id"] for op in sorted_ops] == [1, 2, 3]


def test_sort_by_date_with_invalid_dates(operations_with_invalid_dates: list[dict]) -> None:
    """Тестирование сортировки с некорректными датами."""
    with pytest.raises(ValueError):
        sort_by_date(operations_with_invalid_dates)


def test_sort_by_date_missing_date_key() -> None:
    """Тестирование обработки отсутствия ключа 'date' в операциях."""
    operations = [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-01T12:00:00"},
        {"id": 2, "state": "EXECUTED"},  # Нет ключа 'date'
        {"id": 3, "state": "EXECUTED", "date": "2023-10-03T12:00:00"},
    ]

    with pytest.raises(KeyError, match="Отсутствует ключ 'date'"):
        sort_by_date(operations)
