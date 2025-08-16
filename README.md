# Обработка банковской информации

## Описание

Проект предоставляет набор инструментов для обработки банковских операций:

- **Маскировка данных**: скрытие номеров карт и счетов.
- **Форматирование дат**: приведение дат к удобочитаемому виду.
- **Фильтрация и сортировка**: выборка операций по статусу и сортировка по дате.
- **Генераторы**: эффективная обработка больших объемов транзакций.

## Установка

1. Убедитесь, что у вас установлен [Poetry](https://python-poetry.org/docs/#installation):

```
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

Генераторы

```
from src.generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator
)

# Фильтрация транзакций по валюте
usd_transactions = filter_by_currency(transactions, "USD")
print(next(usd_transactions))

# Получение описаний транзакций
descriptions = transaction_descriptions(transactions)
print(next(descriptions))

# Генерация номеров карт
for card_number in card_number_generator(1, 5):
    print(card_number)  # 0000 0000 0000 0001 ... 0000 0000 0000 0005
```

Декоратор log

Реализован декоратор для логирования выполнения функций:

```python
from src.decorators import log

@log(filename="app.log")  # или @log() для вывода в консоль
def example(arg):
    return arg * 2
```

Логирует:
- Успешное выполнение: `имя_функции ok`
- Ошибки: `имя_функции error: ТипОшибки. Inputs: аргументы`

## Тестирование

Проект покрыт модульными тестами с использованием pytest. Покрытие функционального кода превышает 80%.
Запуск тестов

```
poetry run pytest
```

Отчёт о покрытии

```
poetry run pytest --cov=src --cov-report=html --cov-report=term
```

После выполнения команды:

- В терминале отображается процент покрытия.
- Генерируется папка htmlcov/ с детальным HTML-отчётом.
- Чтобы просмотреть отчёт, откройте файл htmlcov/index.html в браузере.
  Особенности тестовой реализации:
- Использованы фикстуры для подготовки входных данных.
- Применена параметризация (@pytest.mark.parametrize) для проверки различных сценариев.
- Код протестирован на корректные и граничные значения, включая обработку исключений.

## Лицензия

MIT License.
