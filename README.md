# Обработка банковской информации

## Описание
Набор инструментов для обработки банковских данных:
- Маскировка номеров карт и счетов
- Форматирование дат
- Фильтрация и сортировка транзакций

## Установка
Клонируйте репозиторий:
```
git clone https://github.com/NickFedoseev/PythonProject1.git
```
Установите зависимости:
```
pip install -r requirements.txt
```
## Использование
Маскировка данных
```
from src.masks import get_mask_card_number, get_mask_account

print(get_mask_card_number(7000792289606361))  # 7000 79** **** 6361
print(get_mask_account(73654108430135874305))  # **4305
```
Обработка транзакций
```
from src.processing import filter_by_state, sort_by_date

# Фильтрация по статусу
executed_ops = filter_by_state(operations, "EXECUTED")

# Сортировка по дате
sorted_ops = sort_by_date(operations)
```
Форматирование вывода
```
from src.widget import mask_account_card, get_date

print(mask_account_card("Visa Platinum 7000792289606361"))  # Visa Platinum 7000 79** **** 6361
print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
```
## Лицензия MIT
