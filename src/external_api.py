import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


def convert_currency(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли используя Exchange Rates Data API.

    Args:
        transaction (Dict[str, Any]): Словарь с данными о транзакции

    Returns:
        float: Сумма транзакции в рублях

    Raises:
        ValueError: Если не найден API ключ
    """
    # Получаем сумму и валюту из транзакции
    operation_amount = transaction.get("operationAmount", {})
    amount_str = operation_amount.get("amount", "0")
    currency_info = operation_amount.get("currency", {})
    currency_code = currency_info.get("code", "RUB")

    # Конвертируем сумму в float
    try:
        amount = float(amount_str)
    except (ValueError, TypeError):
        amount = 0.0

    # Если валюта уже рубли, возвращаем как есть
    if currency_code == "RUB":
        return amount

    # Если валюта USD или EUR, конвертируем через API
    if currency_code in ["USD", "EUR"]:
        api_key = os.getenv("EXCHANGE_RATES_API_KEY")
        if not api_key:
            raise ValueError("API key not found in environment variables")

        # Формируем запрос к API согласно документации
        url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency_code}&symbols=RUB"
        headers = {"apikey": api_key}

        try:
            # Делаем запрос к API
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Проверяем статус ответа

            data = response.json()

            # Проверяем успешность запроса и наличие нужных данных
            if data.get("success") and "rates" in data and "RUB" in data["rates"]:
                rate = float(data["rates"]["RUB"])
                # Конвертируем сумму
                return amount * rate
            else:
                # Если API вернуло ошибку, возвращаем исходную сумму
                return amount

        except requests.exceptions.RequestException as e:
            # Логируем ошибку (в реальном проекте лучше использовать logging)
            print(f"API request failed: {e}")
            return amount
        except (KeyError, ValueError, TypeError) as e:
            # Обработка ошибок парсинга ответа
            print(f"Error parsing API response: {e}")
            return amount

    # Для других валют возвращаем как есть
    return amount
