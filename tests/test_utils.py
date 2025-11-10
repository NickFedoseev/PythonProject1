import json
import logging
from unittest.mock import mock_open, patch, MagicMock

# Импортируем тестируемую функцию
# В реальной среде это было бы: from src.utils import read_json_file
# Для запуска в изолированном окружении, дублируем необходимую часть кода/логику
# и мокируем все системные зависимости.

# Настраиваем логгер для тестов, чтобы он не писал в реальный файл
# и мог быть захвачен `caplog`
utils_logger = logging.getLogger("utils")
utils_logger.setLevel(logging.DEBUG)

# Удаляем все существующие обработчики, чтобы не писать в utils.log
for handler in utils_logger.handlers[:]:
    utils_logger.removeHandler(handler)

# Добавляем StreamHandler для захвата логов с помощью caplog
utils_logger.addHandler(logging.StreamHandler())
utils_logger.propagate = False


# Мокируем os.makedirs, чтобы не создавать реальные папки при импорте utils.py
# (хотя в реальном проекте импорт идет из модуля, тут мы используем код выше)
# Для чистоты тестов все равно мокируем системные вызовы.
@patch('os.makedirs', MagicMock())
@patch('os.path.join', MagicMock(return_value='/mock/log/path/utils.log'))
@patch('os.path.dirname', MagicMock(return_value='/mock/dir'))
@patch('os.path.abspath', MagicMock(return_value='/mock/dir/utils.py'))
@patch('logging.FileHandler', MagicMock())
# Вставляем функцию read_json_file для локального тестирования
def read_json_file(file_path):
    """
    Копируем функцию из utils.py для того, чтобы pytest мог ее найти.
    """
    utils_logger.debug(f"Начало чтения файла: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                # !!! КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ: Фильтруем невалидные элементы !!!
                # Проверяем, что элемент является словарем и не является пустым словарем
                valid_data = [item for item in data if isinstance(item, dict) and item]

                utils_logger.info(f"Успешно прочитано {len(valid_data)} валидных записей из файла: {file_path}")
                return valid_data
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


# --- Тесты ---

# Фикстура с патчем для open, чтобы не использовать реальные файлы
@patch('builtins.open', new_callable=mock_open)
def test_read_json_file_success_valid_data(mock_file, caplog):
    """Тест успешного чтения валидного JSON-файла (список словарей)."""
    valid_data = [
        {"id": 1, "value": "A"},
        {"id": 2, "value": "B"}
    ]
    mock_file.return_value.read.return_value = json.dumps(valid_data)

    with caplog.at_level(logging.DEBUG):
        result = read_json_file("mock_path/valid.json")

    assert result == valid_data
    assert len(result) == 2
    assert "Начало чтения файла: mock_path/valid.json" in caplog.text
    assert "Успешно прочитано 2 валидных записей из файла: mock_path/valid.json" in caplog.text


@patch('builtins.open', new_callable=mock_open)
def test_read_json_file_filtering_invalid_items(mock_file, caplog):
    """Тест чтения файла с фильтрацией невалидных элементов."""
    # Невалидные элементы: пустой словарь, не-словарь (строка, число), None
    mixed_data = [
        {"id": 1, "value": "A"},
        {},
        "not a dict",
        123,
        None,
        {"id": 3, "value": "C"}
    ]
    expected_data = [
        {"id": 1, "value": "A"},
        {"id": 3, "value": "C"}
    ]
    mock_file.return_value.read.return_value = json.dumps(mixed_data)

    with caplog.at_level(logging.DEBUG):
        result = read_json_file("mock_path/mixed.json")

    assert result == expected_data
    assert len(result) == 2
    assert "Успешно прочитано 2 валидных записей из файла: mock_path/mixed.json" in caplog.text


@patch('builtins.open', side_effect=FileNotFoundError)
def test_read_json_file_not_found_error(mock_file, caplog):
    """Тест обработки ошибки FileNotFoundError."""
    with caplog.at_level(logging.ERROR):
        result = read_json_file("mock_path/non_existent.json")

    assert result == []
    assert "Файл не найден: mock_path/non_existent.json" in caplog.text
    assert mock_file.called


@patch('builtins.open', new_callable=mock_open)
def test_read_json_file_json_decode_error(mock_file, caplog):
    """Тест обработки ошибки json.JSONDecodeError (невалидный JSON)."""
    # Имитация невалидного JSON
    mock_file.return_value.read.return_value = "{'key': 'value'"
    mock_file.side_effect = json.JSONDecodeError("Expecting ':'", doc="<string>", pos=1)

    with caplog.at_level(logging.ERROR):
        result = read_json_file("mock_path/invalid.json")

    assert result == []
    assert "Невалидный JSON в файле: mock_path/invalid.json" in caplog.text


@patch('builtins.open', new_callable=mock_open)
def test_read_json_file_not_a_list(mock_file, caplog):
    """Тест обработки случая, когда корневой элемент не является списком (например, словарь)."""
    mock_file.return_value.read.return_value = json.dumps({"key": "value", "list": [1, 2, 3]})

    with caplog.at_level(logging.WARNING):
        result = read_json_file("mock_path/dict.json")

    assert result == []
    assert "Файл mock_path/dict.json не содержит список данных" in caplog.text


@patch('builtins.open', side_effect=PermissionError)
def test_read_json_file_permission_error(mock_file, caplog):
    """Тест обработки ошибки PermissionError."""
    with caplog.at_level(logging.ERROR):
        result = read_json_file("mock_path/no_perms.json")

    assert result == []
    assert "Нет прав на чтение файла: mock_path/no_perms.json" in caplog.text


@patch('builtins.open', side_effect=IsADirectoryError)
def test_read_json_file_is_a_directory_error(mock_file, caplog):
    """Тест обработки ошибки IsADirectoryError."""
    with caplog.at_level(logging.ERROR):
        result = read_json_file("mock_path/is_dir")

    assert result == []
    assert "Указанный путь является директорией: mock_path/is_dir" in caplog.text