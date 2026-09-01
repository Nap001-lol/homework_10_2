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

# ------------------------------------------------------------------
# filter_by_currency: дополнительные тесты
# ------------------------------------------------------------------

def test_filter_by_currency_no_matches_in_non_empty_list(transactions: List[Dict[str, Any]]) -> None:
    """
    Проверяем, что если в непустом списке нет совпадений по валюте,
    генератор просто ничего не выдаёт (не падает).
    Это покрывает ветку цикла, где условие if ложно для всех элементов.
    """
    gen = filter_by_currency(transactions, "EUR")
    results = list(gen)
    assert results == []


def test_filter_by_currency_mixed_currencies_count(transactions: List[Dict[str, Any]]) -> None:
    """
    Явно проверяем количество совпадений для USD и руб.
    Это дополнительно покрывает ветвление if внутри цикла.
    """
    usd_gen = filter_by_currency(transactions, "USD")
    rub_gen = filter_by_currency(transactions, "руб.")

    assert len(list(usd_gen)) == 3
    assert len(list(rub_gen)) == 2


def test_filter_by_currency_empty_input_list() -> None:
    """
    Пустой список: генератор сразу пуст.
    """
    transactions: List[Dict[str, Any]] = []
    gen = filter_by_currency(transactions)
    results = list(gen)
    assert results == []


def test_filter_by_currency_default_usd(transactions: List[Dict[str, Any]], expected_result_filter_1: Dict[str, Any]) -> None:
    """Проверка фильтрации по умолчанию (USD)"""
    gen = filter_by_currency(transactions)
    assert next(gen) == expected_result_filter_1
    # Проверяем, что вторая тоже USD
    second = next(gen)
    assert second["operationAmount"]["currency"]["name"] == "USD"


# ------------------------------------------------------------------
# transaction_descriptions: дополнительные тесты
# ------------------------------------------------------------------

def test_transaction_descriptions_missing_operation_amount_key() -> None:
    """
    Случай, когда у транзакции вообще нет ключа operationAmount.
    Код должен выбросить KeyError при обращении к transaction["operationAmount"].
    """
    transactions = [
        {"id": 1},  # нет operationAmount
    ]
    gen = transaction_descriptions(transactions)
    with pytest.raises(KeyError):
        next(gen)


def test_transaction_descriptions_all_items_structure(transactions: List[Dict[str, Any]]) -> None:
    """
    Проверяем структуру всех возвращаемых элементов:
    - каждый элемент — dict
    - содержит ключи "amount" и "currency"
    Это покрывает проход по всем элементам списка.
    """
    gen = transaction_descriptions(transactions)
    results = list(gen)

    assert len(results) == len(transactions)
    for item in results:
        assert isinstance(item, dict)
        assert "amount" in item
        assert "currency" in item


def test_transaction_descriptions_single_item_structure() -> None:
    """
    Проверка структуры для одного элемента.
    """
    transactions = [
        {
            "operationAmount": {
                "amount": "100.50",
                "currency": {"name": "USD", "code": "USD"},
            }
        }
    ]
    gen = transaction_descriptions(transactions)
    item = next(gen)
    assert item == {"amount": "100.50", "currency": {"name": "USD", "code": "USD"}}


# ------------------------------------------------------------------
# card_number_generator: дополнительные тесты
# ------------------------------------------------------------------

MAX_LIMIT = 9999999999999999

def test_card_number_generator_boundary_max_limit() -> None:
    """
    Граничный случай: stop == MAX_LIMIT.
    Проверяем, что валидация не ломается и формат корректен.
    """
    start, stop = MAX_LIMIT, MAX_LIMIT
    gen = card_number_generator(start, stop)
    cards = list(gen)
    assert len(cards) == 1
    assert cards[0] == "9999 9999 9999 9999"


def test_card_number_generator_boundary_min_and_max() -> None:
    """
    Минимальный и максимальный диапазон (start=1, stop=MAX_LIMIT).
    Мы не прогоняем весь диапазон, а проверяем только первый и последний элемент,
    чтобы не тормозить тесты. Это покрывает валидацию и форматирование на границах.
    """
    gen_min = card_number_generator(1, 1)
    assert next(gen_min) == "0000 0000 0000 0001"

    gen_max = card_number_generator(MAX_LIMIT, MAX_LIMIT)
    assert next(gen_max) == "9999 9999 9999 9999"


def test_card_number_generator_format_consistency_length_and_spaces() -> None:
    """
    Проверяем длину строки и количество пробелов для разных чисел.
    Это закрывает проверку формата (f-string и разбиение на группы).
    """
    test_values = [1, 1234, 1234567890123456, MAX_LIMIT]
    for value in test_values:
        gen = card_number_generator(value, value)
        card = next(gen)
        # 16 цифр + 3 пробела = 19 символов
        assert len(card) == 19
        assert card.count(" ") == 3
        parts = card.split(" ")
        assert len(parts) == 4
        assert all(len(p) == 4 for p in parts)
        assert all(p.isdigit() for p in parts)


def test_card_number_generator_invalid_start_less_than_1() -> None:
    """
    start < 1 — должно быть ValueError.
    """
    with pytest.raises(ValueError):
        list(card_number_generator(0, 10))


def test_card_number_generator_invalid_stop_greater_than_max() -> None:
    """
    stop > MAX_LIMIT — должно быть ValueError.
    """
    with pytest.raises(ValueError):
        list(card_number_generator(1, MAX_LIMIT + 1))


def test_card_number_generator_start_greater_than_stop() -> None:
    """
    start > stop — должно быть ValueError.
    """
    with pytest.raises(ValueError):
        list(card_number_generator(10, 5))


def test_card_number_generator_small_range_exhaustion() -> None:
    """
    Небольшой диапазон: проверяем, что генератор корректно исчерпывается.
    """
    gen = card_number_generator(5, 7)
    cards = list(gen)
    assert len(cards) == 3
    assert cards[0].endswith("0005")
    assert cards[-1].endswith("0007")


# ------------------------------------------------------------------
# Интеграционные/сводные тесты (опционально, для уверенности)
# ------------------------------------------------------------------

def test_all_generators_empty_input() -> None:
    """
    Все три генератора должны корректно обрабатывать пустой список.
    """
    empty: List[Dict[str, Any]] = []

    assert list(filter_by_currency(empty)) == []
    assert list(transaction_descriptions(empty)) == []

    # card_number_generator не принимает список, но можно проверить валидацию
    with pytest.raises(ValueError):
        list(card_number_generator(0, -1))


def test_filter_by_currency_specific_rub(transactions: List[Dict[str, Any]]) -> None:
    """Проверка фильтрации по конкретной валюте (руб.)"""
    gen = filter_by_currency(transactions, "руб.")
    results = list(gen)
    assert len(results) == 2
    for t in results:
        assert t["operationAmount"]["currency"]["name"] == "руб."


"""Тестирование функции transaction_descriptions"""


def test_transaction_descriptions_basic(transactions: List[Dict[str, Any]]) -> None:
    """Базовая проверка извлечения operationAmount"""
    gen = transaction_descriptions(transactions)
    first = next(gen)
    # Структура должна быть именно operationAmount
    assert first == transactions[0]["operationAmount"]
    assert "amount" in first
    assert "currency" in first


def test_transaction_descriptions_all_items(transactions: List[Dict[str, Any]]) -> None:
    """Проверка, что возвращаются все элементы"""
    gen = transaction_descriptions(transactions)
    results = list(gen)
    assert len(results) == len(transactions)


def test_transaction_descriptions_missing_key() -> None:
    """Проверка выброса KeyError, если нет ключа operationAmount"""
    bad_transactions = [{"id": 1}]  # Нет operationAmount
    gen = transaction_descriptions(bad_transactions)
    with pytest.raises(KeyError):
        next(gen)


def test_transaction_descriptions_empty_list() -> None:
    """Проверка пустого списка"""
    transactions: List[Dict[str, Any]] = []
    gen = transaction_descriptions(transactions)
    assert list(gen) == []


"""Тестирование функции card_number_generator"""


def test_card_number_generator_basic_format(valid_range_small: Tuple[int, int]) -> None:
    """Проверка базового формата и ведущих нулей"""
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


def test_card_number_generator_single_value() -> None:
    """Проверка генерации одного конкретного номера"""
    gen = card_number_generator(1234567890123456, 1234567890123456)
    cards = list(gen)
    assert len(cards) == 1
    assert cards[0] == "1234 5678 9012 3456"


# def test_card_number_generator_boundary_values() -> None:
#     """Проверка граничных значений (минимум и максимум)"""
#     MAX_LIMIT = 9999999999999999

    # Минимум
    gen_min = card_number_generator(1, 1)
    assert next(gen_min) == "0000 0000 0000 0001"

    # Максимум (ИСПРАВЛЕНО: не перебираем весь диапазон, берем конкретный элемент)
    gen_max = card_number_generator(MAX_LIMIT, MAX_LIMIT)
    assert next(gen_max) == "9999 9999 9999 9999"


def test_card_number_generator_invalid_ranges(invalid_ranges: List[Tuple[int, int]]) -> None:
    """Проверка обработки некорректных диапазонов (ValueError)"""
    for start, stop in invalid_ranges:
        with pytest.raises(ValueError):
            # Важно: конвертируем в список, чтобы генератор выполнился и проверил условия
            list(card_number_generator(start, stop))


def test_card_number_generator_format_consistency() -> None:
    """Проверка структуры строки (длина, пробелы, цифры)"""
    test_values = [1, 1234, 1234567890123456, 9999999999999999]
    for value in test_values:
        gen = card_number_generator(value, value)
        card = next(gen)

        # Длина: 16 цифр + 3 пробела = 19 символов
        assert len(card) == 19
        assert card.count(" ") == 3
        parts = card.split(" ")
        assert len(parts) == 4
        assert all(len(p) == 4 for p in parts)
        assert all(p.isdigit() for p in parts)


def test_card_number_generator_exhaustion() -> None:
    """Проверка корректного завершения генератора (StopIteration)"""
    gen = card_number_generator(5, 7)
    cards = list(gen)
    assert len(cards) == 3

    with pytest.raises(StopIteration):
        next(gen)
