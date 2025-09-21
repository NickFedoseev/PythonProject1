import logging
import os

# Определяем корневую директорию проекта (на уровень выше от src/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Создаём папку logs, если её нет
os.makedirs(LOGS_DIR, exist_ok=True)

# Путь к файлу лога
log_file_path = os.path.join(LOGS_DIR, "masks.log")

# Создаём логер именно для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# Создаём обработчик — запись в файл, перезапись при каждом запуске
file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Формат: время - модуль - уровень - сообщение
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# Добавляем обработчик к логеру
logger.addHandler(file_handler)

# Отключаем распространение логов наверх
logger.propagate = False


def get_mask_card_number(card_number: int) -> str:
    """
    Возвращает маскированный номер банковской карты в формате XXXX XX** **** XXXX.
    """
    card_str = str(card_number)
    if len(card_str) != 16:
        logger.error("Ошибка: номер карты должен состоять из 16 цифр")
        raise ValueError("Номер карты должен состоять из 16 цифр")

    first_part = card_str[:6]
    last_part = card_str[-4:]
    masked = f"{first_part[:4]} {first_part[4:6]}** **** {last_part}"
    logger.debug(f"Успешно замаскирован номер карты: {masked}")
    return masked


def get_mask_account(account_number: int) -> str:
    """
    Возвращает маскированный номер банковского счета в формате **XXXX.
    """
    acc_str = str(account_number)
    if len(acc_str) != 20:
        logger.error("Ошибка: номер счета должен состоять из 20 цифр")
        raise ValueError("Номер счета должен состоять из 20 цифр")

    masked = f"**{acc_str[-4:]}"
    logger.debug(f"Успешно замаскирован номер счета: {masked}")
    return masked
