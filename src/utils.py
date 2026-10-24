import json
import logging


def data_json(file_path: str) -> list[dict]:
    """Преобразует данные JSON в Python из data/operations.json"""
    clean_list = []
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                logging.warning(f"JSON содержит не список: {type(data)}")
                return clean_list
            return data
    except FileNotFoundError:
        logging.warning(f"Файл не найден: {file_path}")
        return clean_list
    except json.JSONDecodeError as e:
        logging.warning(f"Ошибка JSON {e}")
        return clean_list


def transaction_amount(transactions_all: list[dict]) -> dict[str, float]:
    """Из полученных данных вычисляет сумму RUB, USD, EUR"""
    transaction_amount_rub = 0
    transaction_amount_usd = 0
    transaction_amount_eur = 0
    for item in transactions_all:
        amount_data = item.get("operationAmount")
        if not amount_data:
            continue
        currency = amount_data.get("currency", {}).get("code")
        try:
            amount = float(amount_data.get("amount", 0))
        except ValueError, TypeError:
            logging.warning(f"Некорректная сумма в транзакции: {amount_data}")
            continue

        if currency == "RUB":
            transaction_amount_rub += amount
        elif currency == "USD":
            transaction_amount_usd += amount
        elif currency == "EUR":
            transaction_amount_eur += amount

    return {
        "amount_RUB": transaction_amount_rub,
        "amount_USD": transaction_amount_usd,
        "amount_EUR": transaction_amount_eur,
    }


def total_rub(transactions_all: list[dict]) -> float:
    """Суммирует все транзакции в рублях (через external_api)"""
    from src.external_api import transaction

    total = 0
    for item in transactions_all:
        rub = transaction(item)
        if rub is not None:
            total += rub
    return total


if __name__ == "__main__":
    my_json = "../data/operations.json"
    transactions = data_json(my_json)
    print("Сумма по валютам:", transaction_amount(transactions))
    print("Итого в рублях:", total_rub(transactions))
