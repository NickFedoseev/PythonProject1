import json
from typing import Any, Dict, List


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с данными о транзакциях.

    Args:
        file_path (str): Путь к JSON-файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
        Если файл пустой, содержит не список или не найден, возвращает пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Проверяем, что данные являются списком
            if isinstance(data, list):
                return data
            else:
                return []

    except FileNotFoundError:
        # Файл не найден
        return []
    except json.JSONDecodeError:
        # Невалидный JSON
        return []
    except PermissionError:
        # Нет прав на чтение файла
        return []
    except IsADirectoryError:
        # Указанный путь является директорией, а не файлом
        return []
    except UnicodeDecodeError:
        # Проблемы с кодировкой
        return []
