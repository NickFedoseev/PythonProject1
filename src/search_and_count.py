import re
from collections import Counter
from typing import Any, Dict, List


def filter_by_description(operations: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Фильтрует операции по заданной строке в описании, используя регулярные выражения.

    Args:
        operations: Список операций (словарей).
        search_string: Строка для поиска в описании.

    Returns:
        Список операций, у которых в описании есть искомая строка.
    """
    if not search_string:
        return operations

    # Использование re.IGNORECASE для поиска без учета регистра
    # re.escape гарантирует, что специальные символы в search_string будут интерпретированы как литералы
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    # Фильтрация списка операций
    return [operation for operation in operations if pattern.search(operation.get("description", ""))]


def count_categories(operations: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество банковских операций для заданных категорий.
    Категория определяется по наличию названия категории в описании операции (description).

    Args:
        operations: Список операций (словарей).
        categories: Список названий категорий для подсчета.

    Returns:
        Словарь, где ключи - названия категорий, а значения - их количество.
    """
    category_counts: Counter[str] = Counter()

    # Создаем паттерны для поиска категорий, игнорируя регистр
    # Используем re.escape для безопасности
    patterns = {category: re.compile(re.escape(category), re.IGNORECASE) for category in categories}

    for operation in operations:
        description = operation.get("description", "")
        for category, pattern in patterns.items():
            # Если категория найдена в описании, увеличиваем счетчик и переходим к следующей операции
            if pattern.search(description):
                category_counts[category] += 1
                break  # Операция относится только к первой найденной категории

    return dict(category_counts)
