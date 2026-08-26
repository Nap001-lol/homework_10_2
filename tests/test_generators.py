from typing import Any, Dict, List, Generator, Tuple

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

"""Тестирование функции filter_by_currency"""


def test_filter_by_currency(
    transactions: List[Dict[str, Any]],
    expected_result_filter_1: Dict[str, Any],
    expected_result_filter_2: Dict[str, Any]
):
    gen = filter_by_currency(transactions)
    assert next(gen) == expected_result_filter_1
    assert next(gen) == expected_result_filter_2


def test_empty_list():
    transactions: List[Dict[str, Any]] = []
    result = list(transaction_descriptions(transactions))
    assert result == []


def test_single_transaction():
    transactions: List[Dict[str, Any]] = [{"operationAmount": 100}]
    result = list(transaction_descriptions(transactions))
    assert result == [100]


def test_multiple_transactions():
    transactions: List[Dict[str, Any]] = [
        {"operationAmount": 10},
        {"operationAmount": 20},
        {"operationAmount": 30},
    ]
    result = list(transaction_descriptions(transactions))
    assert result == [10, 20, 30]


"""Тестирование функции transaction_descriptions"""


def test_transaction_descriptions_first_item(
    transactions: List[Dict[str, Any]],
    expected_result_description_1: Dict[str, Any]
):
    gen = transaction_descriptions(transactions)
    assert next(gen) == expected_result_description_1


def test_transaction_descriptions_second_item(
    transactions: List[Dict[str, Any]],
    expected_result_description_2: Dict[str, Any]
):
    gen = transaction_descriptions(transactions)
    next(gen)  # Пропускаем первый
    assert next(gen) == expected_result_description_2


def test_transaction_descriptions_exhaustion(transactions: List[Dict[str, Any]]):
    gen = transaction_descriptions(transactions)
    # Получаем все элементы
    results = list(gen)

    # Проверяем количество
    assert len(results) == len(transactions)

    # Проверяем, что все элементы имеют правильную структуру
    for item in results:
        assert "amount" in item
        assert "currency" in item


def test_transaction_descriptions_empty_list():
    transactions: List[Dict[str, Any]] = []
    gen = transaction_descriptions(transactions)
    with pytest.raises(StopIteration):
        next(gen)


"""Тестирование функции card_number_generator"""


def test_card_number_generator_basic_format(valid_range_small: Tuple[int, int]):
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


def test_card_number_generator_leading_zeros_and_spaces():
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


def test_card_number_generator_single_value():
    gen = card_number_generator(1234567890123456, 1234567890123456)
    cards = list(gen)
    assert len(cards) == 1
    assert cards[0] == "1234 5678 9012 3456"


def test_card_number_generator_boundary_start():
    gen = card_number_generator(1, 1)
    cards = list(gen)
    assert len(cards) == 1
    assert cards[0] == "0000 0000 0000 0001"


def test_card_number_generator_large_number_format():
    # Пример большого числа, чтобы убедиться, что формат не ломается
    gen = card_number_generator(9999999999999998, 9999999999999999)
    cards = list(gen)
    assert len(cards) == 2
    assert cards[0] == "9999 9999 9999 9998"
    assert cards[1] == "9999 9999 9999 9999"


def test_card_number_generator_invalid_ranges(invalid_ranges: List[Tuple[int, int]]):
    for start, stop in invalid_ranges:
        with pytest.raises(ValueError):
            list(card_number_generator(start, stop))


def test_card_number_generator_exhaustion():
    gen = card_number_generator(100, 102)
    assert next(gen) == "0000 0000 0000 0100"
    assert next(gen) == "0000 0000 0000 0101"
    assert next(gen) == "0000 0000 0000 0102"

    with pytest.raises(StopIteration):
        next(gen)


def test_card_number_generator_step_is_one():
    # Убедимся, что шаг равен 1 (все числа подряд)
    gen = card_number_generator(5, 8)
    cards = list(gen)
    assert len(cards) == 4  # 5,6,7,8
    assert cards[0].endswith("0005")
    assert cards[1].endswith("0006")
    assert cards[2].endswith("0007")
    assert cards[3].endswith("0008")
