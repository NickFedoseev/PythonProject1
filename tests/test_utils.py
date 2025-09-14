import json
from unittest.mock import mock_open, patch

from src.utils import read_json_file


def test_read_json_file_valid() -> None:
    """Тест чтения валидного JSON-файла со списком."""
    test_data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]

    with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
        result = read_json_file("test.json")
        assert result == test_data


def test_read_json_file_empty() -> None:
    """Тест чтения пустого файла."""
    with patch("builtins.open", mock_open(read_data="")):
        result = read_json_file("empty.json")
        assert result == []


def test_read_json_file_not_list() -> None:
    """Тест чтения файла, который не содержит список."""
    test_data = {"id": 1, "amount": 100}

    with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
        result = read_json_file("not_list.json")
        assert result == []


def test_read_json_file_not_found() -> None:
    """Тест чтения несуществующего файла."""
    result = read_json_file("nonexistent.json")
    assert result == []


def test_read_json_file_invalid_json() -> None:
    """Тест чтения файла с невалидным JSON."""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        result = read_json_file("invalid.json")
        assert result == []


def test_read_json_file_permission_error() -> None:
    """Тест обработки ошибки прав доступа."""
    with patch("builtins.open", side_effect=PermissionError("No permission")):
        result = read_json_file("no_permission.json")
        assert result == []


def test_read_json_file_is_a_directory_error() -> None:
    """Тест обработки ошибки при указании директории вместо файла."""
    with patch("builtins.open", side_effect=IsADirectoryError()):
        result = read_json_file("directory/")
        assert result == []


def test_read_json_file_unicode_decode_error() -> None:
    """Тест обработки ошибки декодирования."""
    with patch("builtins.open", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "invalid byte")):
        result = read_json_file("invalid_encoding.json")
        assert result == []
