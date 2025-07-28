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
    # Проверяем минимальную длину и формат до обращения к индексам
    if not date_str or len(date_str) < 10 or date_str[4] != "-" or date_str[7] != "-":
        raise ValueError("Неверный формат даты")

    # Проверяем наличие 'T' только если строка достаточно длинная
    if len(date_str) >= 11 and date_str[10] != "T":
        raise ValueError("Неверный формат даты")

    try:
        year = date_str[0:4]
        month = date_str[5:7]
        day = date_str[8:10]

        # Проверка, что год, месяц и день являются числами
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            raise ValueError("Неверный формат даты")

        month_num = int(month)
        day_num = int(day)

        # Проверка корректности месяца и дня
        if not (1 <= month_num <= 12):
            raise ValueError("Неверный месяц")
        if not (1 <= day_num <= 31):
            raise ValueError("Неверный день")

        return f"{day}.{month}.{year}"
    except ValueError as e:
        if str(e) in ["Неверный месяц", "Неверный день"]:
            raise
        raise ValueError("Неверный формат даты")
