import pytest

from typing import Any, Dict, Generator, List


@pytest.fixture
def transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 789789545,
            "state": "FAMOUS",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "SSD", "code": "SSD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916938",
            "to": "Счет 11776614605963066798",
        },
        {
            "id": 142264288,
            "state": "FAMOUS",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "SSD", "code": "SSD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258543",
            "to": "Счет 75651667383060284189",
        },
    ]


@pytest.fixture
def expected_result_filter_1() -> Dict[str, Any]:
    return {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }


@pytest.fixture
def expected_result_filter_2():
    return {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    }


@pytest.fixture
def expected_result_description_1():
    return {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}}


@pytest.fixture
def expected_result_description_2():
    return {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}}


@pytest.fixture
def valid_range_small():
    """Небольшой диапазон для простых проверок"""
    return 1, 5


@pytest.fixture
def valid_range_with_leading_zeros():
    """Диапазон, где появляются ведущие нули (например, 1 -> 0001...)"""
    return 0, 2  # Обратите внимание: 0 технически выходит за 1<=start, см. ниже тесты


@pytest.fixture
def boundary_values():
    """Граничные значения по ТЗ: 1 и 9999999999999999"""
    return 1, 9999999999999999


@pytest.fixture
def invalid_ranges():
    """Набор некорректных диапазонов для проверки ValueError"""
    return [
        (0, 10),  # start < 1
        (1, 10000000000000000),  # stop > 9999999999999999
        (10, 5),  # start > stop
        (-5, 10),  # start < 1
    ]
