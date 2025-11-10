import os
from typing import Any, Dict, List

from src.decorators import log
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.search_and_count import filter_by_description
from src.transaction_readers import read_transactions_from_csv, read_transactions_from_excel
from src.utils import read_json_file
from src.widget import get_date, mask_account_card

# Константы
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "data", "operations.json")
CSV_PATH = os.path.join(BASE_DIR, "data", "transactions.csv")  # Предполагаемый путь
XLSX_PATH = os.path.join(BASE_DIR, "data", "transactions_excel.xlsx")  # Предполагаемый путь
LOG_MAIN_PATH = os.path.join(BASE_DIR, "logs/log_main.txt")
AVAILABLE_STATUSES = ["EXECUTED", "CANCELED", "PENDING"]


def get_transactions_data() -> List[Dict[str, Any]]:
    """
    Запрашивает у пользователя выбор источника данных и возвращает список транзакций.
    """
    print("Программа: Привет! Добро пожаловать в программу работы")
    print("с банковскими транзакциями.")

    while True:
        print("Выберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        file_choice = input("Пользователь: ").strip()

        if file_choice == "1":
            print("Программа: Для обработки выбран JSON-файл.")
            return read_json_file(JSON_PATH)
        elif file_choice == "2":
            print("Программа: Для обработки выбран CSV-файл.")
            # В реальном проекте здесь может понадобиться обработка FileNotFoundError
            return read_transactions_from_csv(CSV_PATH)
        elif file_choice == "3":
            print("Программа: Для обработки выбран XLSX-файл.")
            # В реальном проекте здесь может понадобиться обработка FileNotFoundError
            return read_transactions_from_excel(XLSX_PATH)
        else:
            print("Программа: Неверный выбор. Пожалуйста, введите 1, 2 или 3.")


def get_filter_status() -> str:
    """
    Запрашивает у пользователя статус для фильтрации с проверкой корректности.
    """
    while True:
        print("\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(AVAILABLE_STATUSES)}")

        user_status_input = input("Пользователь: ").strip().upper()

        if user_status_input in AVAILABLE_STATUSES:
            print(f'Программа: Операции отфильтрованы по статусу "{user_status_input}"')
            return user_status_input
        else:
            print(f'Программа: Статус операции "{user_status_input}" недоступен.')


def ask_yes_no(prompt: str) -> bool:
    """
    Запрашивает у пользователя ответ Да/Нет.
    """
    while True:
        user_input = input(f"Программа: {prompt} Да/Нет\nПользователь: ").strip().lower()
        if user_input in ("да", "да."):
            return True
        elif user_input in ("нет", "нет."):
            return False
        else:
            print("Программа: Пожалуйста, ответьте 'Да' или 'Нет'.")


def ask_sort_order() -> bool:
    """
    Запрашивает у пользователя порядок сортировки (по возрастанию/по убыванию).
    Возвращает True для убывания (от новых к старым), False для возрастания.
    """
    while True:
        print("Программа: Отсортировать по возрастанию или по убыванию?")
        user_input = input("Пользователь: ").strip().lower()

        if "убыванию" in user_input:
            # Сортировка по убыванию: reverse=True (от новых к старым)
            return True
        elif "возрастанию" in user_input:
            # Сортировка по возрастанию: reverse=False (от старых к новым)
            return False
        else:
            print("Программа: Пожалуйста, введите 'по возрастанию' или 'по убыванию'.")


def format_transaction_output(transaction: Dict[str, Any]) -> str:
    """
    Форматирует одну транзакцию для вывода в консоль.
    """
    date_formatted = get_date(transaction.get("date", ""))
    description = transaction.get("description", "")

    # Форматирование "откуда"
    from_info = transaction.get("from", "Неизвестно")
    if from_info != "Неизвестно":
        try:
            from_masked = mask_account_card(from_info)
        except ValueError:
            from_masked = from_info  # Если не удалось замаскировать, оставляем как есть
    else:
        from_masked = "Источник не указан"

    # Форматирование "куда"
    to_info = transaction.get("to", "Счет **????")
    try:
        to_masked = mask_account_card(to_info)
    except ValueError:
        to_masked = to_info  # Если не удалось замаскировать, оставляем как есть

    # Сумма и валюта
    amount_data = transaction.get("operationAmount", {})
    amount = amount_data.get("amount", "0.00")
    currency_name = amount_data.get("currency", {}).get("name", "руб.")

    # Если есть "from", показываем стрелку, иначе показываем только "to"
    if "from" in transaction:
        source_target_line = f"{from_masked} -> {to_masked}"
    else:
        source_target_line = f"Счет {to_masked.split('**')[-1]}"  # Показываем только Счет **XXXX

    # Конвертация в рубли (если валюта USD/EUR) - для демонстрации использования external_api
    final_amount = float(amount)
    if currency_name != "руб.":
        # Этот вызов просто демонстрирует использование external_api,
        # но для вывода используем исходную сумму и валюту, как в примере задания.
        # final_amount = convert_currency(transaction)
        pass

    output = [f"{date_formatted} {description}", source_target_line, f"Сумма: {final_amount:.2f} {currency_name}"]
    return "\n".join(output)


@log(filename=LOG_MAIN_PATH)
def main() -> None:
    """
    Основная логика программы: взаимодействие с пользователем, фильтрация и вывод транзакций.
    """
    # ----------------------------------------------------
    # Тестовые вызовы для генерации логов в masks.log
    # Это сделано, чтобы продемонстрировать, что masks.py пишет в свой лог-файл
    try:
        get_mask_card_number(1234567812345678)
        get_mask_account(12345678901234567890)
    except ValueError:
        # Ошибки здесь игнорируются, чтобы не провоцировать лог 'main error'
        pass
    # ----------------------------------------------------

    # 1. Получение данных
    all_transactions = get_transactions_data()

    if not all_transactions:
        print("\nПрограмма: Не удалось получить данные о транзакциях. Программа завершается.")
        return

    # 2. Фильтрация по статусу
    filter_status = get_filter_status()
    filtered_transactions = filter_by_state(all_transactions, filter_status)

    # 3. Дополнительные фильтры и сортировка

    # Сортировка по дате
    if ask_yes_no("Отсортировать операции по дате?"):
        reverse_sort = ask_sort_order()  # True = по убыванию (новые к старым)
        filtered_transactions = sort_by_date(filtered_transactions, reverse=reverse_sort)

    # Фильтрация по рублям
    if ask_yes_no("Выводить только рублевые транзакции?"):
        filtered_transactions = [
            t for t in filtered_transactions if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]

    # Фильтрация по слову в описании
    if ask_yes_no("Отфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("Программа: Введите слово для поиска:\nПользователь: ").strip()
        filtered_transactions = filter_by_description(filtered_transactions, search_word)

    # 4. Вывод результата
    print("\nПрограмма: Распечатываю итоговый список транзакций...")
    print("\nПрограмма:")

    if not filtered_transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши\nусловия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}\n")

    for transaction in filtered_transactions:
        # Здесь также вызывается mask_account_card, которая вызывает get_mask_card_number/account,
        # что также инициирует логирование в masks.log
        print(format_transaction_output(transaction))
        print()  # Дополнительный перенос строки для разделения транзакций


if __name__ == "__main__":
    main()
