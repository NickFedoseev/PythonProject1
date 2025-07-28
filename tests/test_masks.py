import pytest

from src.masks import get_mask_account, get_mask_card_number


# Фикстура для корректных номеров карт
@pytest.fixture
def valid_card_numbers() -> list[tuple[int, str]]:
    return [
        (7000792289606361, "7000 79** **** 6361"),
        (1234567890123456, "1234 56** **** 3456"),
        (1111222233334444, "1111 22** **** 4444"),
    ]


# Фикстура для некорректных номеров карт
@pytest.fixture
def invalid_card_numbers() -> list[tuple[int, str]]:
    return [
        (12345678901234, "Номер карты должен состоять из 16 цифр"),  # Слишком короткий
        (12345678901234567890, "Номер карты должен состоять из 16 цифр"),  # Слишком длинный
        (0, "Номер карты должен состоять из 16 цифр"),  # Ноль
    ]


# Фикстура для корректных номеров счетов
@pytest.fixture
def valid_account_numbers() -> list[tuple[int, str]]:
    return [
        (73654108430135874305, "**4305"),
        (12345678901234567890, "**7890"),
        (11112222333344445555, "**5555"),
    ]


# Фикстура для некорректных номеров счетов
@pytest.fixture
def invalid_account_numbers() -> list[tuple[int, str]]:
    return [
        (123456789012345678, "Номер счета должен состоять из 20 цифр"),  # Слишком короткий
        (1234567890123456789012, "Номер счета должен состоять из 20 цифр"),  # Слишком длинный
        (0, "Номер счета должен состоять из 20 цифр"),  # Ноль
    ]


# Тесты для get_mask_card_number
@pytest.mark.parametrize(
    "card_number, expected",
    [
        (7000792289606361, "7000 79** **** 6361"),
        (1234567890123456, "1234 56** **** 3456"),
        (1111222233334444, "1111 22** **** 4444"),
    ],
)
def test_get_mask_card_number_valid(card_number: int, expected: str) -> None:
    """Проверка маскирования корректных номеров карт."""
    assert get_mask_card_number(card_number) == expected


def test_get_mask_card_number_valid_from_fixture(valid_card_numbers: list[tuple[int, str]]) -> None:
    """Проверка маскирования корректных номеров карт из фикстуры."""
    for card_number, expected in valid_card_numbers:
        result = get_mask_card_number(card_number)
        assert result == expected
        assert len(result) == 19  # Формат: XXXX XX** **** XXXX
        assert result[4] == " " and result[8] == "*" and result[14] == " "  # Проверка структуры
        assert result[10:14] == "****"  # Проверка маски


@pytest.mark.parametrize(
    "card_number, expected_error",
    [
        (12345678901234, "Номер карты должен состоять из 16 цифр"),
        (12345678901234567890, "Номер карты должен состоять из 16 цифр"),
        (0, "Номер карты должен состоять из 16 цифр"),
    ],
)
def test_get_mask_card_number_invalid(card_number: int, expected_error: str) -> None:
    """Проверка обработки некорректных номеров карт."""
    with pytest.raises(ValueError, match=expected_error):
        get_mask_card_number(card_number)


def test_get_mask_card_number_invalid_from_fixture(invalid_card_numbers: list[tuple[int, str]]) -> None:
    """Проверка обработки некорректных номеров карт из фикстуры."""
    for card_number, expected_error in invalid_card_numbers:
        with pytest.raises(ValueError, match=expected_error):
            get_mask_card_number(card_number)


# Тесты для get_mask_account
@pytest.mark.parametrize(
    "account_number, expected",
    [
        (73654108430135874305, "**4305"),
        (12345678901234567890, "**7890"),
        (11112222333344445555, "**5555"),
    ],
)
def test_get_mask_account_valid(account_number: int, expected: str) -> None:
    """Проверка маскирования корректных номеров счетов."""
    assert get_mask_account(account_number) == expected


def test_get_mask_account_valid_from_fixture(valid_account_numbers: list[tuple[int, str]]) -> None:
    """Проверка маскирования корректных номеров счетов из фикстуры."""
    for account_number, expected in valid_account_numbers:
        result = get_mask_account(account_number)
        assert result == expected
        assert len(result) == 6  # Формат: **XXXX
        assert result.startswith("**")  # Проверка маски
        assert result[2:].isdigit()  # Проверка, что последние 4 символа — цифры


@pytest.mark.parametrize(
    "account_number, expected_error",
    [
        (123456789012345678, "Номер счета должен состоять из 20 цифр"),
        (1234567890123456789012, "Номер счета должен состоять из 20 цифр"),
        (0, "Номер счета должен состоять из 20 цифр"),
    ],
)
def test_get_mask_account_invalid(account_number: int, expected_error: str) -> None:
    """Проверка обработки некорректных номеров счетов."""
    with pytest.raises(ValueError, match=expected_error):
        get_mask_account(account_number)


def test_get_mask_account_invalid_from_fixture(invalid_account_numbers: list[tuple[int, str]]) -> None:
    """Проверка обработки некорректных номеров счетов из фикстуры."""
    for account_number, expected_error in invalid_account_numbers:
        with pytest.raises(ValueError, match=expected_error):
            get_mask_account(account_number)
