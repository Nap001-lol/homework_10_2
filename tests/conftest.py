from typing import Any, Dict, List, Tuple

import pytest


@pytest.fixture
def transactions() -> List[Dict[str, Any]]:
    return  [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
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
def expected_result_filter_2() -> Dict[str, Any]:
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
def expected_result_description_1() -> Dict[str, Any]:
    return {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}}


@pytest.fixture
def expected_result_description_2() -> Dict[str, Any]:
    return {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}}


@pytest.fixture
def valid_range_small() -> Tuple[int, int]:
    """Небольшой диапазон для простых проверок"""
    return 1, 5


@pytest.fixture
def valid_range_with_leading_zeros() -> Tuple[int, int]:
    """Диапазон, где появляются ведущие нули (например, 1 -> 0001...)"""
    return 0, 2  # Обратите внимание: 0 технически выходит за 1<=start, см. ниже тесты


@pytest.fixture
def boundary_values() -> Tuple[int, int]:
    """Граничные значения по ТЗ: 1 и 9999999999999999"""
    return 1, 9999999999999999


@pytest.fixture
def invalid_ranges() -> List[Tuple[int, int]]:
    """Набор некорректных диапазонов для проверки ValueError"""
    return [
        (0, 10),  # start < 1
        (1, 10000000000000000),  # stop > 9999999999999999
        (10, 5),  # start > stop
        (-5, 10),  # start < 1
    ]
