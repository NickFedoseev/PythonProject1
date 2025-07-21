import pytest

from src.widget import get_date, mask_account_card


# Фикстура для корректных входных данных для mask_account_card
@pytest.fixture
def valid_account_card_data():
    return [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
        ("Account 73654108430135874305", "Account **4305"),
        ("Checking Account 12345678901234567890", "Checking Account **7890"),
    ]


# Фикстура для некорректных входных данных для mask_account_card
@pytest.fixture
def invalid_account_card_data():
    return [
        ("Visa", "Неверный формат входных данных"),  # Слишком мало частей
        ("", "Неверный формат входных данных"),  # Пустая строка
        ("Visa Platinum 123abc", "Последняя часть должна быть числом"),  # Нечисловой номер
        ("Visa Platinum 12345678901234", "Неверная длина номера"),  # Слишком короткий номер
        ("Checking Account 1234567890123456789012", "Неверная длина номера"),  # Слишком длинный номер
    ]


# Фикстура для корректных входных данных для get_date
@pytest.fixture
def valid_date_data():
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-01T00:00:00.000", "01.12.2023"),
        ("2025-01-31T23:59:59", "31.01.2025"),
        ("2022-06-15T12:34:56.123456789", "15.06.2022"),
    ]


# Фикстура для некорректных входных данных для get_date
@pytest.fixture
def invalid_date_data():
    return [
        ("", "Неверный формат даты"),  # Пустая строка
        ("2024-03-1", "Неверный формат даты"),  # Слишком короткая
        ("2024/03-11T02:26:18", "Неверный формат даты"),  # Неверный разделитель
        ("2024-03-11X02:26:18", "Неверный формат даты"),  # Отсутствует T
        ("2024-abc-11T02:26:18", "Неверный формат даты"),  # Нечисловой месяц
        ("2024-03-1aT02:26:18", "Неверный формат даты"),  # Нечисловой день
        ("2024-00-11T02:26:18", "Неверный месяц"),  # Некорректный месяц
        ("2024-13-11T02:26:18", "Неверный месяц"),  # Некорректный месяц
        ("2024-03-00T02:26:18", "Неверный день"),  # Некорректный день
        ("2024-03-32T02:26:18", "Неверный день"),  # Некорректный день
    ]


# Тесты для mask_account_card
@pytest.mark.parametrize("input_str, expected", [
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
    ("Account 73654108430135874305", "Account **4305"),
    ("Checking Account 12345678901234567890", "Checking Account **7890"),
])
def test_mask_account_card_valid(input_str, expected):
    """Проверка маскирования корректных номеров карт и счетов."""
    assert mask_account_card(input_str) == expected


def test_mask_account_card_valid_from_fixture(valid_account_card_data):
    """Проверка маскирования корректных номеров карт и счетов из фикстуры."""
    for input_str, expected in valid_account_card_data:
        result = mask_account_card(input_str)
        assert result == expected
        parts = result.split()
        assert len(parts) >= 2  # Минимум тип и замаскированный номер
        if len(parts[-1]) == 19:  # Формат карты: XXXX XX** **** XXXX
            assert parts[-1][4] == " " and parts[-1][8] == "*" and parts[-1][15] == " "
            assert parts[-1][11:15] == "****"
        elif len(parts[-1]) == 6:  # Формат счета: **XXXX
            assert parts[-1].startswith("**")
            assert parts[-1][2:].isdigit()


@pytest.mark.parametrize("input_str, expected_error", [
    ("Visa", "Неверный формат входных данных"),
    ("", "Неверный формат входных данных"),
    ("Visa Platinum 123abc", "Последняя часть должна быть числом"),
    ("Visa Platinum 12345678901234", "Неверная длина номера"),
    ("Checking Account 1234567890123456789012", "Неверная длина номера"),
])
def test_mask_account_card_invalid(input_str, expected_error):
    """Проверка обработки некорректных входных данных."""
    with pytest.raises(ValueError, match=expected_error):
        mask_account_card(input_str)


def test_mask_account_card_invalid_from_fixture(invalid_account_card_data):
    """Проверка обработки некорректных входных данных из фикстуры."""
    for input_str, expected_error in invalid_account_card_data:
        with pytest.raises(ValueError, match=expected_error):
            mask_account_card(input_str)


# Тесты для get_date
@pytest.mark.parametrize("input_str, expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2023-12-01T00:00:00.000", "01.12.2023"),
    ("2025-01-31T23:59:59", "31.01.2025"),
    ("2022-06-15T12:34:56.123456789", "15.06.2022"),
])
def test_get_date_valid(input_str, expected):
    """Проверка преобразования корректных дат."""
    assert get_date(input_str) == expected


def test_get_date_valid_from_fixture(valid_date_data):
    """Проверка преобразования корректных дат из фикстуры."""
    for input_str, expected in valid_date_data:
        result = get_date(input_str)
        assert result == expected
        assert len(result) == 10  # Формат: ДД.ММ.ГГГГ
        assert result[2] == "." and result[5] == "."  # Проверка разделителей
        # Проверка, что день, месяц, год — цифры
        assert result[:2].isdigit() and result[3:5].isdigit() and result[6:].isdigit()


@pytest.mark.parametrize("input_str, expected_error", [
    ("", "Неверный формат даты"),
    ("2024-03-1", "Неверный формат даты"),
    ("2024/03-11T02:26:18", "Неверный формат даты"),
    ("2024-03-11X02:26:18", "Неверный формат даты"),
    ("2024-abc-11T02:26:18", "Неверный формат даты"),
    ("2024-03-1aT02:26:18", "Неверный формат даты"),
    ("2024-00-11T02:26:18", "Неверный месяц"),
    ("2024-13-11T02:26:18", "Неверный месяц"),
    ("2024-03-00T02:26:18", "Неверный день"),
    ("2024-03-32T02:26:18", "Неверный день"),
])
def test_get_date_invalid(input_str, expected_error):
    """Проверка обработки некорректных дат."""
    with pytest.raises(ValueError, match=expected_error):
        get_date(input_str)


def test_get_date_invalid_from_fixture(invalid_date_data):
    """Проверка обработки некорректных дат из фикстуры."""
    for input_str, expected_error in invalid_date_data:
        with pytest.raises(ValueError, match=expected_error):
            get_date(input_str)
