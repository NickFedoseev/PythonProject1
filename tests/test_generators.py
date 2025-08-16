# tests/test_generators.py

from collections.abc import Iterator

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

# --- Фикстуры ---


@pytest.fixture
def sample_transactions() -> list[dict]:
    """Пример списка транзакций с разными валютами."""
    return [
        {
            "operationAmount": {
                "currency": {"code": "USD"},
                "amount": "100.00",
            },
            "description": "Payment 1",
        },
        {
            "operationAmount": {
                "currency": {"code": "EUR"},
                "amount": "200.00",
            },
            "description": "Payment 2",
        },
        {
            "operationAmount": {
                "currency": {"code": "USD"},
                "amount": "300.00",
            },
            "description": "Payment 3",
        },
    ]


@pytest.fixture
def empty_transactions() -> list:
    """Пустой список транзакций."""
    return []


# --- Тесты для filter_by_currency ---


@pytest.mark.parametrize(
    "currency, expected_descriptions",
    [
        ("USD", ["Payment 1", "Payment 3"]),
        ("EUR", ["Payment 2"]),
        ("GBP", []),
    ],
)
def test_filter_by_currency_filters_correctly(
    sample_transactions: list[dict], currency: str, expected_descriptions: list[str]
) -> None:
    """Проверяет, что фильтрация по валюте возвращает правильные транзакции."""
    result = filter_by_currency(sample_transactions, currency)
    assert isinstance(result, Iterator)
    descriptions = [t["description"] for t in list(result)]
    assert descriptions == expected_descriptions


def test_filter_by_currency_empty_list(empty_transactions: list) -> None:
    """Проверяет, что фильтрация пустого списка возвращает пустой результат."""
    result = filter_by_currency(empty_transactions, "USD")
    assert list(result) == []


def test_filter_by_currency_no_match(sample_transactions: list[dict]) -> None:
    """Проверяет, что при отсутствии совпадений возвращается пустой список."""
    result = filter_by_currency(sample_transactions, "JPY")
    assert list(result) == []


# --- Тесты для transaction_descriptions ---


@pytest.mark.parametrize(
    "transactions, expected",
    [
        (
            [
                {"description": "A"},
                {"description": "B"},
            ],
            ["A", "B"],
        ),
        ([], []),
        (
            [{"description": "Оплата"}],
            ["Оплата"],
        ),
    ],
)
def test_transaction_descriptions_returns_descriptions(transactions: list[dict], expected: list[str]) -> None:
    """Проверяет, что функция возвращает список описаний транзакций."""
    result = transaction_descriptions(transactions)
    assert isinstance(result, Iterator)
    assert list(result) == expected


# --- Тесты для card_number_generator ---


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (9999, 9999, ["0000 0000 0000 9999"]),
        (0, 1, ["0000 0000 0000 0000", "0000 0000 0000 0001"]),
        (
            1234567890123456,
            1234567890123458,
            ["1234 5678 9012 3456", "1234 5678 9012 3457", "1234 5678 9012 3458"],
        ),
    ],
)
def test_card_number_generator_generates_correct_format(start: int, stop: int, expected: list[str]) -> None:
    """Проверяет, что генератор выдаёт правильные номера карт в нужном формате."""
    result = card_number_generator(start, stop)
    assert isinstance(result, Iterator)
    assert list(result) == expected


def test_card_number_generator_invalid_range() -> None:
    """Проверяет, что при start > stop выбрасывается ошибка."""
    with pytest.raises(ValueError, match="Начальное значение не может быть больше конечного."):
        list(card_number_generator(10, 5))


def test_card_number_generator_negative_numbers() -> None:
    """Проверяет, что при отрицательных числах выбрасывается ошибка."""
    with pytest.raises(ValueError, match="Номера карт не могут быть отрицательными."):
        list(card_number_generator(-1, 5))


def test_card_number_generator_too_large_number() -> None:
    """Проверяет, что при числе >= 10^16 выбрасывается ошибка."""
    with pytest.raises(ValueError, match="Числа должны быть меньше 10\\^16, чтобы уместиться в 16 цифр."):
        list(card_number_generator(10**16 - 1, 10**16))
    with pytest.raises(ValueError, match="Числа должны быть меньше 10\\^16, чтобы уместиться в 16 цифр."):
        list(card_number_generator(10**16, 10**16))
