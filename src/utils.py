import json
import logging
from pathlib import Path

# Создаем папку logs
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Настраиваем логгер модуля
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем хендлер для файла
file_handler = logging.FileHandler(LOG_DIR / "utils.log", mode="w", encoding="utf-8")

# Создаем форматтер для файла
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавляем хендлер к логгеру
logger.addHandler(file_handler)


def data_json(file_path: str) -> list[dict]:
    """Преобразует данные JSON в Python из data/operations.json"""
    clean_list: list[dict] = []
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                logger.warning(f"JSON содержит не список: {type(data)}")
                return clean_list
            return data
    except FileNotFoundError:
        logger.warning(f"Файл не найден: {file_path}")
        return clean_list
    except json.JSONDecodeError as e:
        logger.warning(f"Ошибка JSON {e}")
        return clean_list


def transaction_amount(transactions_all: list[dict]) -> dict[str, float]:
    """Из полученных данных вычисляет сумму RUB, USD, EUR"""
    transaction_amount_rub = 0.0
    transaction_amount_usd = 0.0
    transaction_amount_eur = 0.0
    for item in transactions_all:
        amount_data = item.get("operationAmount")
        if not amount_data:
            continue
        currency = amount_data.get("currency", {}).get("code")
        try:
            amount = float(amount_data.get("amount", 0))
        except (ValueError, TypeError):
            logger.warning(f"Некорректная сумма в транзакции: {amount_data}")
            continue

        if currency == "RUB":
            transaction_amount_rub += amount
        elif currency == "USD":
            transaction_amount_usd += amount
        elif currency == "EUR":
            transaction_amount_eur += amount

    result = {
        "amount_RUB": transaction_amount_rub,
        "amount_USD": transaction_amount_usd,
        "amount_EUR": transaction_amount_eur,
    }
    logger.info(f"Код выполнен. Результат: {result}")
    return result


def total_rub(transactions_all: list[dict]) -> float:
    """Суммирует все транзакции в рублях (через external_api)"""
    from src.external_api import transaction

    total = 0.0
    for item in transactions_all:
        rub = transaction(item)
        if rub is not None:
            total += rub
    logger.info(f"Код выполнен. Результат: {total}")
    return total


if __name__ == "__main__":
    my_json = "../data/operations.json"
    transactions = data_json(my_json)
    print("Сумма по валютам:", transaction_amount(transactions))
    print("Итого в рублях:", total_rub(transactions))
