import json
import logging
import os
from typing import Any, Dict, List

# Определяем корневую директорию проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
log_file_path = os.path.join(LOGS_DIR, "utils.log")

# Создаём логер
utils_logger = logging.getLogger("utils")
utils_logger.setLevel(logging.DEBUG)

# Обработчик
file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Форматтер
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# Добавляем handler
utils_logger.addHandler(file_handler)
utils_logger.propagate = False  # отключаем распространение


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    utils_logger.debug(f"Начало чтения файла: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                utils_logger.info(f"Успешно прочитано {len(data)} записей из файла: {file_path}")
                return data
            else:
                utils_logger.warning(f"Файл {file_path} не содержит список данных")
                return []

    except FileNotFoundError:
        utils_logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError:
        utils_logger.error(f"Невалидный JSON в файле: {file_path}")
        return []
    except PermissionError:
        utils_logger.error(f"Нет прав на чтение файла: {file_path}")
        return []
    except IsADirectoryError:
        utils_logger.error(f"Указанный путь является директорией: {file_path}")
        return []
    except UnicodeDecodeError:
        utils_logger.error(f"Проблемы с кодировкой файла: {file_path}")
        return []
    except Exception as e:
        utils_logger.error(f"Неизвестная ошибка при чтении файла {file_path}: {e}")
        return []
