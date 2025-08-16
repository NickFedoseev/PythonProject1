import os
from typing import NoReturn

import pytest

from src.decorators import log


def test_log_to_console(capsys: pytest.CaptureFixture[str]) -> None:
    """Тестирует логирование в консоль при успешном выполнении"""

    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(2, 3)
    captured = capsys.readouterr()
    assert "add ok" in captured.out
    assert result == 5


def test_log_to_file() -> None:
    """Тестирует запись логов в файл"""
    test_file = "test.log"

    @log(filename=test_file)
    def div(a: int, b: int) -> float:
        return a / b

    # Удаляем старый лог-файл если есть
    if os.path.exists(test_file):
        os.remove(test_file)

    div(10, 2)  # Вызываем тестируемую функцию

    # Проверяем содержимое файла
    with open(test_file, "r") as f:
        content = f.read()

    assert "div ok" in content
    os.remove(test_file)  # Удаляем тестовый файл


def test_error_logging(capsys: pytest.CaptureFixture[str]) -> None:
    """Тестирует логирование ошибок"""

    @log()
    def fail() -> NoReturn:
        raise ValueError("Test error")

    try:
        fail()
    except ValueError:
        pass

    captured = capsys.readouterr()
    assert "fail error: ValueError" in captured.out
    assert "Inputs: (), {}" in captured.out
