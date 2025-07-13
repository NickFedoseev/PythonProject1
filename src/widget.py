from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_account: str) -> str:
    """
    Принимает строку с типом и номером карты или счета.
    Возвращает строку с замаскированным номером.
    """
    parts = card_or_account.split()
    if len(parts) < 2:
        raise ValueError("Неверный формат входных данных")

    number = parts[-1]
    if not number.isdigit():
        raise ValueError("Последняя часть должна быть числом")

    name = " ".join(parts[:-1])

    if len(number) == 16:
        masked = get_mask_card_number(int(number))
    elif len(number) == 20:
        masked = get_mask_account(int(number))
    else:
        raise ValueError("Неверная длина номера")

    return f"{name} {masked}"


def get_date(date_str: str) -> str:
    """
    Принимает строку с датой в формате '2024-03-11T02:26:18.671407'
    Возвращает дату в формате 'ДД.ММ.ГГГГ', например '11.03.2024'
    """
    year = date_str[0:4]  # Год — первые 4 символа
    month = date_str[5:7]  # Месяц — символы 5 и 6
    day = date_str[8:10]  # День — символы 8 и 9

    return f"{day}.{month}.{year}"


if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))  # Visa Platinum 7000 79** **** 6361
    print(get_date("2024-03-11T02:26:18.671407"))  # Вывод: 11.03.2024
