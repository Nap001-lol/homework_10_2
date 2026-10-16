import json


def data_json(file_path):
    """Преобразует данные JSON в Python из data/operations.json"""
    clean_list = []
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return clean_list
    except json.JSONDecodeError as e:
        return clean_list


# if __name__ == '__main__':
#     my_json = "../data/operations.json"
#     print(data_json(my_json))


def transaction_amount(transactions: list) -> dict:
    """Из полученных данных вычисляет сумму RUB, USD, EUR"""
    transaction_amount_rub = 0
    transaction_amount_usd = 0
    transaction_amount_eur = 0
    for item in transactions:
        amount_data = item.get("operationAmount")
        if not amount_data
            continue
        currency = amount_data.get("currency", {}).get("code")
        amount = float(amount_data.get("amount", 0))

        if currency == "RUB":
            transaction_amount_rub += amount
        elif currency == "USD":
            transaction_amount_usd += amount
        elif currency == "EUR":
            transaction_amount_eur += amount


    return [{'amount_RUB': transaction_amount_rub, 'amount_USD': transaction_amount_usd, 'amount_EUR': transaction_amount_eur}]


# if __name__ == '__main__':
#     my_json = "../data/operations.json"
#     transactions = data_json(my_json)
#     print(transaction_amount(transactions))
