import requests
from src.utils import transaction_amount
import os
from dotenv import load_dotenv

load_dotenv('.env')
API_KEY = os.getenv('API_KEY')

def transaction_from_usd():
    amount_usd = transaction_amount()[1]
    url = "https://api.apilayer.com/exchangerates_data/convert"

    payload = {
        "from": "USD",
        "to": "RUB",
        "amount": amount_usd
    }

    headers= {
        "apikey": API_KEY
    }

    response = requests.get(url, headers=headers, params=payload)

    try:
        return response.json()['result']
    except KeyError:
        return 'Сумма изменяемой валюты равна 0!'


def transaction_from_eur():

    amount_eur = transaction_amount()[2]

    url = "https://api.apilayer.com/exchangerates_data/convert"

    payload = {
        "from": "USD",
        "to": "RUB",
        "amount": amount_eur
    }

    headers= {
    "apikey": API_KEY
    }

    response = requests.get(url, headers=headers, params=payload)

    try:
        return response.json()['result']
    except KeyError:
        return 'Сумма изменяемой валюты равна 0!'

if __name__ == '__main__':
    print(transaction_from_eur())
