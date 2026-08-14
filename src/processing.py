"""Функция filter_by_state, которая принимает список словарей и опционально значение для ключа
state (по умолчанию 'EXECUTED').Функция возвращает новый список словарей, содержащий только те словари, у которых ключ
state соответствует указанному значению."""

from datetime import datetime
from typing import Any, Dict, List, Union


def filter_by_state(date_list: List[Dict[str, Any]], state: str = "EXECUTED") -> Union[List[Dict[str, Any]], str]:
    """Функция возвращает новый список словарей, содержащий только те словари, у которых ключ state
    соответствует указанному значению"""
    new_list = []
    count = 0
    for data in date_list:
        if data["state"] == state:
            new_list.append(data)
            count += 1
    if count > 0:
        return new_list
    else:
        return "Ключ не соответствует значениям в словаре"


"""Функция sort_by_date, которая принимает список словарей и необязательный параметр, задающий порядок сортировки
(по умолчанию — убывание). Функция должна возвращать новый список, отсортированный по дате (date)."""


def sort_by_date(date_list: List[Dict[str, Any]], date_reverse: bool = True) -> List[Dict[str, Any]]:
    """Функция возвращает новый список, отсортированный по дате (date)"""
    return sorted(date_list, key=lambda i: datetime.fromisoformat(i["date"]), reverse=date_reverse)


if __name__ == "__main__":
    print(
        filter_by_state(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            "CANCELED",
        )
    )
    print(
        sort_by_date(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ]
        )
    )
