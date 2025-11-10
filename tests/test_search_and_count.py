from typing import Any, Dict, List

import pytest

# Исправленный импорт: используем имена функций из src/search_and_count.py
from src.search_and_count import count_categories, filter_by_description


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {"description": "Перевод организации", "amount": 100},
        {"description": "Открытие вклада", "amount": 200},
        {"description": "Перевод с карты на карту", "amount": 300},
        {"description": "Покупка в магазине", "amount": 50},
    ]


def test_filter_by_description_found(sample_transactions: List[Dict[str, Any]]) -> None:
    # Используем правильное имя функции: filter_by_description
    result = filter_by_description(sample_transactions, "Перевод")
    assert len(result) == 2
    assert all("Перевод" in tx["description"] for tx in result)


def test_filter_by_description_case_insensitive(sample_transactions: List[Dict[str, Any]]) -> None:
    # Используем правильное имя функции: filter_by_description
    result = filter_by_description(sample_transactions, "перевод")
    assert len(result) == 2


def test_filter_by_description_not_found(sample_transactions: List[Dict[str, Any]]) -> None:
    # Используем правильное имя функции: filter_by_description
    result = filter_by_description(sample_transactions, "Зарплата")
    assert result == []


def test_filter_by_description_empty_search(sample_transactions: List[Dict[str, Any]]) -> None:
    # Используем правильное имя функции: filter_by_description
    result = filter_by_description(sample_transactions, "")
    assert result == sample_transactions


def test_count_categories(sample_transactions: List[Dict[str, Any]]) -> None:
    # Используем правильное имя функции: count_categories
    categories = ["Перевод", "вклад", "Покупка"]
    result = count_categories(sample_transactions, categories)
    # Обратите внимание: функция count_categories чувствительна к поисковой строке,
    # ищет точное совпадение в описании (без учета регистра),
    # поэтому "Покупка в магазине" будет соответствовать категории "Покупка".
    expected = {"Перевод": 2, "вклад": 1, "Покупка": 1}
    assert result == expected
