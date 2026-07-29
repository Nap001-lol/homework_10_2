"""Пример для карты
Visa Platinum 7000792289606361  # входной аргумент
Visa Platinum 7000 79 ** ** ** 6361  # выход функции

Пример для счета
Счет 73654108430135874305  # входной аргумент
Счет ** 4305  # выход функции
"""

from datetime import datetime

from masks import get_mask_account, get_mask_card_number


def mask_account_card(card_data: str) -> str:
    """Функция, котрая обрабатывает информацию о картах(счетах)"""

    list_card_data = card_data.split()
    mask_card_data = []
    for i in list_card_data:
        if i.isalpha():
            mask_card_data.append(i)
        elif i.isdigit():
            if len(i) == 16:
                list_digit_mask_card = get_mask_card_number(i)
                mask_card_data.append(list_digit_mask_card)
            elif len(i) == 20:
                mask_card_data.append(get_mask_account(i))
            else:
                return "Введены некоректные данные"
        else:
            return "Введены некоректные данные"
    return " ".join(mask_card_data)


def get_data(iso_string: str) -> str:
    str_string_data = datetime.fromisoformat(iso_string)
    return str(str_string_data)[8:10] + "." + str(str_string_data)[5:7] + "." + str(str_string_data)[:4]


if __name__ == "__main__":
    print(mask_account_card("MasterCard 7158300734726758"))
    print(get_data("2024-03-11T02:26:18.671407"))
