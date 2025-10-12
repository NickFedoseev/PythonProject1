from typing import Any, Dict, List

import pandas as pd


def read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла.

    Args:
        file_path (str): Путь к CSV-файлу.

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями.
    """
    df = pd.read_csv(file_path, sep=";")
    result: List[Dict[str, Any]] = df.to_dict(orient="records")  # type: ignore[assignment]
    return result


def read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel-файла (.xlsx).

    Args:
        file_path (str): Путь к XLSX-файлу.

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями.
    """
    df = pd.read_excel(file_path)
    result: List[Dict[str, Any]] = df.to_dict(orient="records")  # type: ignore[assignment]
    return result
