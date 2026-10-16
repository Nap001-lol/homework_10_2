import logging
import os
from pathlib import Path
import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

def _get_api_key() -> str:
    return os.getenv("API_KEY")


def transaction(payload: dict[str, str]) -> float | None:
    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": _get_api_key()}

    try:
        response = requests.get(url, headers=headers, params=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Ошибка при запросе к API: {e}")
        return None

    data = response.json()
    if "result" not in data:
        logging.error(f'Неожиданный ответ API: {data}')
        return None
    return data["result"]


if __name__ == '__main__':
    payload = {
    "from": "USD",
    "to": "RUB",
    "amount": 100
    }

    result = transaction(payload)
    if result is not None:
        print(f"Результат конвертации: {result}")
    else:
        print("Конвертация не удалась")
