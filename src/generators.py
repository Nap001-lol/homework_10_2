from typing import Any, Dict, List, Generator


def filter_by_currency(transactions: List[Dict[str, Any]], state: str = "USD") -> Generator[Dict[str, Any]]:
    """Функция, которая принимает на вход список словарей, а выдает поочередно транзакции по заданной операции"""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["name"] == state:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[Dict[str, Any]]:
    """Принимает список словарей с транзакциями и возвращает описание каждой операции по очереди"""
    for transaction in transactions:
        yield transaction["operationAmount"]


def card_number_generator(start: int, stop: int):
    """
    Генератор для создания номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    Параметры:
    start (int): начальное значение диапазона (минимум 1)
    stop (int): конечное значение диапазона (максимум 9999999999999999)

    Возвращает отформатированный номер карты в виде строки.
    """
    # Проверяем корректность входных данных
    if not (1 <= start <= stop <= 9999999999999999):
        raise ValueError("Некорректный диапазон номеров карт")

    # Генерируем номера карт в заданном диапазоне
    for number in range(start, stop + 1):
        # Форматируем число в строку с ведущими нулями
        formatted_number = f"{number:016d}"
        # Разбиваем на группы по 4 символа и добавляем пробелы
        card_number = f"{formatted_number[:4]} {formatted_number[4:8]} {formatted_number[8:12]} {formatted_number[12:]}"
        yield card_number
