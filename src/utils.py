import json


def data_json(file_path="../data/operations.json"):
    clean_list = []
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Файл json отсутствует")
        return clean_list
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
        return clean_list


def transaction_amount():
    transaction_amount_rub = 0
    transaction_amount_usd = 0
    transaction_amount_eur = 0
    for item in data_json():
        operation_amount = item.get("operationAmount")
        if operation_amount and operation_amount.get("currency", {}).get("code") == "RUB":
            transaction_amount_rub += float(operation_amount["amount"])
        elif operation_amount and operation_amount.get("currency", {}).get("code") == "USD":
            transaction_amount_usd += float(operation_amount["amount"])
        elif operation_amount and operation_amount.get("currency", {}).get("code") == "EUR":
            transaction_amount_eur += float(operation_amount["amount"])

    return [transaction_amount_rub, transaction_amount_usd, transaction_amount_eur]


if __name__ == "__main__":
    print(transaction_amount())
