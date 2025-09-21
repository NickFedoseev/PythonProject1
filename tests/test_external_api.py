import os
from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest
import requests

from src.external_api import convert_currency


def test_convert_currency_rub() -> None:
    """Тест конвертации рублей (без конвертации)."""
    transaction = {"operationAmount": {"amount": "100.0", "currency": {"code": "RUB"}}}
    result = convert_currency(transaction)
    assert result == 100.0


def test_convert_currency_rub_without_currency_code() -> None:
    """Тест конвертации без указания кода валюты."""
    transaction = {"operationAmount": {"amount": "100.0", "currency": {}}}
    result = convert_currency(transaction)
    assert result == 100.0


def test_convert_currency_invalid_amount() -> None:
    """Тест конвертации с невалидной суммой."""
    transaction = {"operationAmount": {"amount": "invalid", "currency": {"code": "RUB"}}}
    result = convert_currency(transaction)
    assert result == 0.0


def test_convert_currency_missing_operation_amount() -> None:
    """Тест конвертации при отсутствии operationAmount."""
    transaction: Dict[str, Any] = {}
    result = convert_currency(transaction)
    assert result == 0.0


@patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"})
@patch("src.external_api.requests.get")
def test_convert_currency_usd_success(mock_get: MagicMock) -> None:
    """Тест успешной конвертации USD в RUB."""
    # Мокируем успешный ответ API
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True, "rates": {"RUB": 90.0}, "base": "USD"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    transaction = {"operationAmount": {"amount": "10.0", "currency": {"code": "USD"}}}
    result = convert_currency(transaction)

    assert result == 900.0
    mock_get.assert_called_once()


@patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"})
@patch("src.external_api.requests.get")
def test_convert_currency_eur_success(mock_get: MagicMock) -> None:
    """Тест успешной конвертации EUR в RUB."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True, "rates": {"RUB": 100.0}, "base": "EUR"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    transaction = {"operationAmount": {"amount": "5.0", "currency": {"code": "EUR"}}}
    result = convert_currency(transaction)

    assert result == 500.0
    mock_get.assert_called_once()


@patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"})
@patch("src.external_api.requests.get")
def test_convert_currency_api_failure(mock_get: MagicMock) -> None:
    """Тест обработки неуспешного ответа API."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": False, "error": {"info": "Invalid API key"}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    transaction = {"operationAmount": {"amount": "10.0", "currency": {"code": "USD"}}}
    result = convert_currency(transaction)

    assert result == 10.0  # Должен вернуть исходную сумму


@patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"})
@patch("src.external_api.requests.get")
def test_convert_currency_api_missing_rub_rate(mock_get: MagicMock) -> None:
    """Тест обработки отсутствия курса RUB в ответе API."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True, "rates": {"EUR": 0.9}, "base": "USD"}  # Нет RUB в rates
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    transaction = {"operationAmount": {"amount": "10.0", "currency": {"code": "USD"}}}
    result = convert_currency(transaction)

    assert result == 10.0  # Должен вернуть исходную сумму


@patch.dict(os.environ, {"EXCHANGE_RATES_API_KEY": "test_key"})
@patch("src.external_api.requests.get")
def test_convert_currency_api_request_exception(mock_get: MagicMock) -> None:
    """Тест обработки исключения при запросе к API."""
    # Мокируем исключение при вызове requests.get
    mock_get.side_effect = requests.exceptions.RequestException("API error")

    transaction = {"operationAmount": {"amount": "10.0", "currency": {"code": "USD"}}}
    result = convert_currency(transaction)

    assert result == 10.0  # Должен вернуть исходную сумму


def test_convert_currency_no_api_key() -> None:
    """Тест отсутствия API ключа."""
    if "EXCHANGE_RATES_API_KEY" in os.environ:
        del os.environ["EXCHANGE_RATES_API_KEY"]

    transaction = {"operationAmount": {"amount": "10.0", "currency": {"code": "USD"}}}

    with pytest.raises(ValueError, match="API key not found"):
        convert_currency(transaction)


def test_convert_currency_other_currency() -> None:
    """Тест конвертации для валюты, отличной от USD/EUR."""
    transaction = {"operationAmount": {"amount": "50.0", "currency": {"code": "GBP"}}}  # Фунт стерлингов
    result = convert_currency(transaction)

    assert result == 50.0  # Должен вернуть исходную сумму
