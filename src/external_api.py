import os

import requests
from dotenv import load_dotenv

from src.utils import transaction_amount

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")


def transaction(payload):
    url = "https://api.apilayer.com/exchangerates_data/convert"

    headers = {"apikey": API_KEY}

    response = requests.get(url, headers=headers, params=payload)

    try:
        return response.json()["result"]
    except KeyError:
        return "Сумма изменяемой валюты равна 0!"


if __name__ == "__main__":
    print(transaction({"from": "USD", "to": "RUB", "amount": transaction_amount()[1]}))
