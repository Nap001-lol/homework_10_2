"""Пример для карты
Visa Platinum 7000792289606361  # входной аргумент
Visa Platinum 7000 79 ** ** ** 6361  # выход функции

Пример для счета
Счет 73654108430135874305  # входной аргумент
Счет ** 4305  # выход функции
"""

from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_data: str) -> str:
    """Функция, которая обрабатывает информацию о картах(счетах)"""

    card_data_parts = card_data.split()
    masked_data = []
    isalpha_in_card_data = 0
    digit_in_card_data = 0
    for data in card_data_parts:
        if data.isalpha() and isalpha_in_card_data < 1:
            masked_data.append(data)
            isalpha_in_card_data += 1
        elif data.isdigit():
            if len(data) == 16:
                list_digit_mask_card = get_mask_card_number(data)
                masked_data.append(list_digit_mask_card)
                digit_in_card_data += 1
            elif len(data) == 20:
                masked_data.append(get_mask_account(data))
                digit_in_card_data += 1
            else:
                return "Введены некорректные данные"
        else:
            return "Введены некорректные данные"
    if digit_in_card_data > 1:
        return "Введены некорректные данные"
    return " ".join(masked_data)


def get_data(iso_string: str) -> str:
    """Функция, форматирования iso формата"""
    str_data = datetime.fromisoformat(iso_string)
    return str(str_data)[8:10] + "." + str(str_data)[5:7] + "." + str(str_data)[:4]


if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(get_data("2024-03-11T02:26:18.671407"))
