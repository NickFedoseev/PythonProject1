def get_mask_card_number(card_number: int) -> str:
    """
    Возвращает маскированный номер банковской карты в формате XXXX XX** **** XXXX.
    """
    card_str = str(card_number)
    if len(card_str) != 16:
        raise ValueError("Номер карты должен состоять из 16 цифр")

    first_part = card_str[:6]
    last_part = card_str[-4:]
    return f"{first_part[:4]} {first_part[4:6]}** **** {last_part}"


def get_mask_account(account_number: int) -> str:
    """
    Возвращает маскированный номер банковского счета в формате **XXXX.
    """
    acc_str = str(account_number)
    if len(acc_str) != 20:
        raise ValueError("Номер счета должен состоять из 20 цифр")
    return f"**{acc_str[-4:]}"
