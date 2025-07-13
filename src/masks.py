def get_mask_card_number(card_number: int) -> str:
    """
    Возвращает маскированный номер банковской карты в формате XXXX XX** **** XXXX.
    """
    card_str = str(card_number)
    first_part = card_str[:6]
    last_part = card_str[-4:]
    return f"{first_part[:4]} {first_part[4:6]}** **** {last_part}"


def get_mask_account(account_number: int) -> str:
    """
    Возвращает маскированный номер банковского счета в формате **XXXX.
    """
    acc_str = str(account_number)
    return f"**{acc_str[-4:]}"


if __name__ == "__main__":
    print(get_mask_card_number(7000792289606361))  # 7000 79** **** 6361
    print(get_mask_account(73654108430135874305))  # **4305
