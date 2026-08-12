import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def executed_transactions():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

@pytest.fixture
def canceled_transactions():
    return [
        {"id": 41428829, "state": "CANCELED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "CANCELED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

@pytest.fixture
def transactions_without_state():
    """Список, где у одного элемента нет ключа 'state' — для проверки KeyError"""
    return [
        {"id": 41428829, "date": "2019-07-03T18:35:29.512364"},  # нет state
        {"id": 41428830, "state": "EXECUTED", "date": "2019-07-04T10:00:00"},
    ]

@pytest.fixture
def empty_transactions():
    return []

@pytest.fixture
def single_transaction():
    return [{"id": 99, "date": "2023-12-31T23:59:59"}]

@pytest.fixture
def duplicate_dates_transactions():
    return [
        {"id": 1, "date": "2023-01-01T10:00:00"},
        {"id": 2, "date": "2023-01-01T10:00:00"},
        {"id": 3, "date": "2022-01-01T10:00:00"},
    ]

@pytest.fixture
def invalid_date_format_transactions():
    return [
        {"id": 1, "date": "01-01-2023"},
        {"id": 2, "date": "2023/01/01"},
    ]

@pytest.fixture
def missing_date_key_transactions():
    return [
        {"id": 1},  # нет date
        {"id": 2, "date": "2023-01-01T10:00:00"},
    ]

def test_filter_by_state():
    assert (filter_by_state(
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        ]) ==
            ([
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}
            ]))

    assert (filter_by_state(
        [
            {"id": 41428829, "state": "CANCELED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "CANCELED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        ])) == "Ключ не соответствует значениям в словаре"

    @pytest.mark.parametrize(
        "data_list, state, expected_result, expect_error",
        [
            # Сценарий 1: Есть совпадения
            (
                    [
                        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}
                    ],
                    "EXECUTED",
                    [{"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}],
                    False
            ),

            # Сценарий 2: Пустой список
            (
                    [],
                    "EXECUTED",
                    "Ключ не соответствует значениям в словаре",
                    False
            ),

            # Сценарий 3: В словаре отсутствует ключ 'state' (вызовет KeyError)
            (
                    [
                        {"id": 41428829, "date": "2019-07-03T18:35:29.512364"},  # нет ключа state
                        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}
                    ],
                    "EXECUTED",
                    None,  # результат не важен, так как ожидается ошибка
                    True
            ),
        ]
    )
    def test_filter(data_list, state, expected_result, expect_error):
        if expect_error:
            with pytest.raises(KeyError):
                filter_by_state(data_list, state)
        else:
            result = filter_by_state(data_list, state)
            assert result == expected_result

def test_empty_list():
    """Функция должна возвращать пустой список, если входной список пуст"""
    assert sort_by_date([]) == []


def test_single_item():
    """Список из одного элемента должен остаться неизменным"""
    data = [{"id": 99, "date": "2023-12-31T23:59:59"}]
    assert sort_by_date(data) == data


def test_duplicate_dates():
    """При одинаковых датах порядок элементов должен сохраняться (стабильная сортировка)"""
    data = [
        {"id": 1, "date": "2023-01-01T10:00:00"},
        {"id": 2, "date": "2023-01-01T10:00:00"},  # Та же дата
        {"id": 3, "date": "2022-01-01T10:00:00"}
    ]
    result = sort_by_date(data, date_reverse=True)
    # Проверяем, что даты отсортированы верно
    dates = [item["date"] for item in result]
    assert dates[0] == "2023-01-01T10:00:00"
    assert dates[1] == "2023-01-01T10:00:00"
    assert dates[2] == "2022-01-01T10:00:00"

    # Важно: Python использует стабильную сортировку.
    # Элементы с одинаковыми датами должны сохранить свой относительный порядок.
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2

def test_invalid_date_format():
    """Функция должна выбросить ValueError, если дата не в формате ISO"""
    bad_data = [
        {"id": 1, "date": "01-01-2023"}, # Неверный формат
        {"id": 2, "date": "2023/01/01"}  # Неверный разделитель
    ]
    with pytest.raises(ValueError):
        sort_by_date(bad_data)

def test_missing_date_key():
    """Функция должна выбросить KeyError, если ключа 'date' нет в словаре"""
    incomplete_data = [
        {"id": 1}, # Нет поля date
        {"id": 2, "date": "2023-01-01T10:00:00"}
    ]
    with pytest.raises(KeyError):
        sort_by_date(incomplete_data)