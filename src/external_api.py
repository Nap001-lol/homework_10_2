import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _get_api_key() -> str:
    """Возвращает API-ключ из .env или None"""
    return os.getenv("API_KEY")


def _convert_to_rub(amount: float, currency: str) -> float | None:
    """Конвертирует сумму из валюты в RUB через API apilayer"""
    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": _get_api_key()}
    payload = {"from": currency, "to": "RUB", "amount": amount}

    try:
        response = requests.get(url, headers=headers, params=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе к API: {e}")
        return None

    data = response.json()
    if "result" not in data:
        logging.error(f"Неожиданный ответ API: {data}")
        return None
    return data["result"]


def transaction(transaction_all: dict) -> float | None:
    """Принимает транзакию, возвращает сумму в рублях. RUB возвращается напрямую, USD/EUR - конвертируется через API"""
    amount_data = transaction_all.get("operationAmount")

    if not amount_data:
        logging.warning("В транзакции нет operationAmount")
        return None

    try:
        amount = float(amount_data.get("amount", 0))
    except ValueError, TypeError:
        logging.warning(f"Некорректная сумма: {amount_data}")
        return None

    currency = amount_data.get("currency", {}).get("code")
    if currency == "RUB":
        return amount
    if currency in ("EUR", "USD"):
        return _convert_to_rub(amount, currency)

    logging.warning(f"Неизвестная валюта: {currency}")
    return None
