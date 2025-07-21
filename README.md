# Обработка банковской информации

## Описание
Проект предоставляет набор инструментов для обработки банковских операций:
- **Маскировка данных**: скрытие номеров карт и счетов.
- **Форматирование дат**: приведение дат к удобочитаемому виду.
- **Фильтрация и сортировка**: выборка операций по статусу и сортировка по дате.

## Установка
1. Убедитесь, что у вас установлен [Poetry](https://python-poetry.org/docs/#installation):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
2. Клонируйте репозиторий:
```
git clone https://github.com/NickFedoseev/PythonProject1.git
cd PythonProject1
```
3. Установите зависимости:
```
poetry install
```
4. Активируйте виртуальное окружение:
```
poetry shell
```
## Использование
Маскировка данных
```
from src.masks import get_mask_card_number, get_mask_account

# Маскировка номера карты (16 цифр)
print(get_mask_card_number(7000792289606361))  # 7000 79** **** 6361

# Маскировка номера счёта (20 цифр)
print(get_mask_account(73654108430135874305))  # **4305
```
Обработка транзакций
```
from src.processing import filter_by_state, sort_by_date

operations = [
    {"id": 1, "state": "EXECUTED", "date": "2024-01-01"},
    {"id": 2, "state": "CANCELED", "date": "2024-02-01"}
]

# Фильтрация по статусу (по умолчанию — EXECUTED)
executed_ops = filter_by_state(operations)
print(executed_ops)  # [{'id': 1, 'state': 'EXECUTED', 'date': '2024-01-01'}]

# Сортировка по дате (по умолчанию — новые сначала)
sorted_ops = sort_by_date(operations)
print(sorted_ops)  # [{'id': 2, ...}, {'id': 1, ...}]
```
Форматирование вывода
```
from src.widget import mask_account_card, get_date

# Маскировка номера карты/счёта из строки
print(mask_account_card("Visa Platinum 7000792289606361"))  # Visa Platinum 7000 79** **** 6361

# Преобразование даты в формат DD.MM.YYYY
print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
```
##Запуск тестов
```
poetry run pytest
```
## Лицензия 
MIT License.
