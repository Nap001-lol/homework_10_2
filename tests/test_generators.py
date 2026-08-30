from typing import Any, Dict, List, Tuple

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

"""Тестирование функции filter_by_currency"""


def test_filter_by_currency(
    transactions: List[Dict[str, Any]],
    expected_result_filter_1: Dict[str, Any],
    expected_result_filter_2: Dict[str, Any],
) -> None:
    gen = filter_by_currency(transactions)
    assert next(gen) == expected_result_filter_1
    assert next(gen) == expected_result_filter_2


def test_empty_list() -> None:
    transactions: List[Dict[str, Any]] = []
    result = list(transaction_descriptions(transactions))
    assert result == []


def test_single_transaction() -> None:
    transactions: List[Dict[str, Any]] = [{"operationAmount": 100}]
    result = list(transaction_descriptions(transactions))
    assert result == [100]


def test_multiple_transactions() -> None:
    transactions: List[Dict[str, Any]] = [
        {"operationAmount": 10},
        {"operationAmount": 20},
        {"operationAmount": 30},
    ]
    result = list(transaction_descriptions(transactions))
    assert result == [10, 20, 30]

    def test_filter_by_currency_different_currency(transactions: List[Dict[str, Any]]) -> None:
        gen = filter_by_currency(transactions, "RUB")
        result = list(gen)
        assert len(result) == 2  # Должны быть 2 транзакции в RUB

    def test_filter_by_currency_no_matches(transactions: List[Dict[str, Any]]) -> None:
        gen = filter_by_currency(transactions, "EUR")
        result = list(gen)
        assert result == []  # Нет транзакций в EUR

    def test_filter_by_currency_empty_list() -> None:
        transactions: List[Dict[str, Any]] = []
        gen = filter_by_currency(transactions)
        with pytest.raises(StopIteration):
            next(gen)


"""Тестирование функции transaction_descriptions"""


def test_transaction_descriptions_first_item(
    transactions: List[Dict[str, Any]], expected_result_description_1: Dict[str, Any]
) -> None:
    gen = transaction_descriptions(transactions)
    assert next(gen) == expected_result_description_1


def test_transaction_descriptions_second_item(
    transactions: List[Dict[str, Any]], expected_result_description_2: Dict[str, Any]
) -> None:
    gen = transaction_descriptions(transactions)
    next(gen)  # Пропускаем первый
    assert next(gen) == expected_result_description_2


def test_transaction_descriptions_exhaustion(transactions: List[Dict[str, Any]]) -> None:
    gen = transaction_descriptions(transactions)
    # Получаем все элементы
    results = list(gen)

    # Проверяем количество
    assert len(results) == len(transactions)

    # Проверяем, что все элементы имеют правильную структуру
    for item in results:
        assert "amount" in item
        assert "currency" in item


def test_transaction_descriptions_empty_list() -> None:
    transactions: List[Dict[str, Any]] = []
    gen = transaction_descriptions(transactions)
    with pytest.raises(StopIteration):
        next(gen)


def test_transaction_descriptions_invalid_structure() -> None:
    transactions = [
        {"operationAmount": {"amount": 100}},  # Отсутствует currency
        {"operationAmount": {"currency": {"name": "USD"}}},  # Отсутствует amount
    ]
    gen = transaction_descriptions(transactions)

    # Проверяем, что генератор не падает при неполных данных
    results = list(gen)
    assert len(results) == 2
    assert "amount" in results[0]
    assert "currency" in results[1]


def test_transaction_descriptions_large_numbers() -> None:
    transactions = [
        {"operationAmount": {"amount": "9999999999999999", "currency": {"name": "USD"}}},
        {"operationAmount": {"amount": "0.0000000001", "currency": {"name": "USD"}}}
    ]
    gen = transaction_descriptions(transactions)
    results = list(gen)
    assert len(results) == 2
    assert results[0]["amount"] == "9999999999999999"
    assert results[1]["amount"] == "0.0000000001"


"""Тестирование функции card_number_generator"""


def test_card_number_generator_basic_format(valid_range_small: Tuple[int, int]) -> None:
    start, stop = valid_range_small
    gen = card_number_generator(start, stop)

    expected = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]
    result = list(gen)
    assert result == expected


def test_card_number_generator_leading_zeros_and_spaces() -> None:
    # Проверяем, что форматирование работает корректно даже для маленьких чисел
    gen = card_number_generator(1, 3)
    cards = list(gen)
    assert len(cards) == 3
    assert cards[0] == "0000 0000 0000 0001"
    assert cards[1] == "0000 0000 0000 0002"
    assert cards[2] == "0000 0000 0000 0003"

    # Проверка структуры: ровно 4 группы по 4 цифры, разделённые пробелами
    for card in cards:
        parts = card.split()
        assert len(parts) == 4
        assert all(len(p) == 4 for p in parts)
        assert all(p.isdigit() for p in parts)


def test_card_number_generator_single_value() -> None:
    gen = card_number_generator(1234567890123456, 1234567890123456)
    cards = list(gen)
    assert len(cards) == 1
    assert cards[0] == "1234 5678 9012 3456"


def test_card_number_generator_boundary_start() -> None:
    gen = card_number_generator(1, 1)
    cards = list(gen)
    assert len(cards) == 1
    assert cards[0] == "0000 0000 0000 0001"


def test_card_number_generator_large_number_format() -> None:
    # Пример большого числа, чтобы убедиться, что формат не ломается
    gen = card_number_generator(9999999999999998, 9999999999999999)
    cards = list(gen)
    assert len(cards) == 2
    assert cards[0] == "9999 9999 9999 9998"
    assert cards[1] == "9999 9999 9999 9999"


def test_card_number_generator_invalid_ranges(invalid_ranges: List[Tuple[int, int]]) -> None:
    for start, stop in invalid_ranges:
        with pytest.raises(ValueError):
            list(card_number_generator(start, stop))


def test_card_number_generator_exhaustion() -> None:
    gen = card_number_generator(100, 102)
    assert next(gen) == "0000 0000 0000 0100"
    assert next(gen) == "0000 0000 0000 0101"
    assert next(gen) == "0000 0000 0000 0102"

    with pytest.raises(StopIteration):
        next(gen)


def test_card_number_generator_step_is_one() -> None:
    # Убедимся, что шаг равен 1 (все числа подряд)
    gen = card_number_generator(5, 8)
    cards = list(gen)
    assert len(cards) == 4  # 5,6,7,8
    assert cards[0].endswith("0005")
    assert cards[1].endswith("0006")
    assert cards[2].endswith("0007")
    assert cards[3].endswith("0008")


def test_card_number_generator_max_range() -> None:
    start, stop = 9999999999999998, 9999999999999999
    gen = card_number_generator(start, stop)
    result = list(gen)
    assert len(result) == 2
    assert result[0] == "9999 9999 9999 9998"
    assert result[1] == "9999 9999 9999 9999"
