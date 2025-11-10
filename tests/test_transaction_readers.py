from typing import Any, Dict, List
from unittest.mock import patch

import pandas as pd
import pytest

# Импортируем функции чтения, которые мы хотим протестировать
from src.transaction_readers import read_transactions_from_csv, read_transactions_from_excel


@pytest.fixture
def mock_dataframe() -> pd.DataFrame:
    """Фикстура, создающая мок-объект DataFrame."""
    data = {
        "id": [1, 2],
        "date": ["2023-01-01", "2023-01-02"],
        "description": ["Test 1", "Test 2"],
    }
    return pd.DataFrame(data)


# Строка 7: test_read_transactions_from_csv (вероятно)
def test_read_transactions_from_csv_success(mock_dataframe: pd.DataFrame) -> None:
    """Тест успешного чтения из CSV."""
    with patch("pandas.read_csv", return_value=mock_dataframe) as mock_read:
        result = read_transactions_from_csv("dummy_path.csv")
        mock_read.assert_called_once()

        expected: List[Dict[str, Any]] = [
            {"id": 1, "date": "2023-01-01", "description": "Test 1"},
            {"id": 2, "date": "2023-01-02", "description": "Test 2"},
        ]
        assert result == expected


# Строка 15: test_read_transactions_from_excel (вероятно)
def test_read_transactions_from_excel_success(mock_dataframe: pd.DataFrame) -> None:
    """Тест успешного чтения из Excel."""
    with patch("pandas.read_excel", return_value=mock_dataframe) as mock_read:
        result = read_transactions_from_excel("dummy_path.xlsx")
        mock_read.assert_called_once()

        expected: List[Dict[str, Any]] = [
            {"id": 1, "date": "2023-01-01", "description": "Test 1"},
            {"id": 2, "date": "2023-01-02", "description": "Test 2"},
        ]
        assert result == expected
