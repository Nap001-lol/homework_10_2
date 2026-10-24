from typing import List

import pytest

from src.widget import get_data, mask_account_card


def test_mask_account_card() -> None:
    """Тестирование функции, которая обрабатывает информацию о картах(счетах)"""
    assert mask_account_card("VisaPlatinum 7000792289606361") == "VisaPlatinum 7000 79** **** 6361"
    assert mask_account_card(("Счет 73654108430135874305")) == "Счет **4305"
    assert mask_account_card("Maestro 1596837868705199") == "Maestro 1596 83** **** 5199"
    assert mask_account_card("Счет 64686473678894779589") == "Счет **9589"
    assert mask_account_card("MasterCard 7158300734726758") == "MasterCard 7158 30** **** 6758"
    assert mask_account_card("Счет 35383033474447895560") == "Счет **5560"
    assert mask_account_card("111111") == "Введены некорректные данные"
    assert mask_account_card("Счет 35383033474447895560 35383033474447895560") == "Введены некорректные данные"
    assert mask_account_card("Счет Счет 35383033474447895560") == "Введены некорректные данные"
    assert mask_account_card("Счет 35383033474447895560 Счет") == "Введены некорректные данные"


@pytest.fixture
def valid_iso_dates() -> List[str]:
    """Фикстура, возвращающая список валидных ISO строк для тестирования"""
    return [
        "2023-10-05",
        "1999-01-31",
        "2000-12-01",
        "2024-02-29",  # Високосный год
    ]


@pytest.fixture
def expected_results() -> List[str]:
    """Фикстура с ожидаемыми результатами в формате DD.MM.YYYY"""
    return [
        "05.10.2023",
        "31.01.1999",
        "01.12.2000",
        "29.02.2024",
    ]


# --- Тесты ---


def test_get_data_valid_dates(valid_iso_dates: List[str], expected_results: List[str]) -> None:
    """Проверка работы функции на наборе валидных дат"""
    for iso_str, expected in zip(valid_iso_dates, expected_results):
        result = get_data(iso_str)
        assert result == expected, f"Ошибка для даты {iso_str}: ожидалось {expected}, получено {result}"


def test_get_data_single_case() -> None:
    """Проверка конкретного случая без использования фикстур (для разнообразия)"""
    iso_input = "2021-07-15"
    expected_output = "15.07.2021"
    assert get_data(iso_input) == expected_output


def test_get_data_invalid_format() -> None:
    """Проверка обработки неверного формата (должно выбрасываться ValueError)"""
    invalid_input = "05.10.2023"  # Не ISO формат
    with pytest.raises(ValueError):
        get_data(invalid_input)


def test_get_data_empty_string() -> None:
    """Проверка обработки пустой строки"""
    with pytest.raises(ValueError):
        get_data("")


# Параметризованный тест (более современный подход вместо фикстур для простых кейсов)
@pytest.mark.parametrize(
    "iso_input, expected_output",
    [
        ("2022-03-08", "08.03.2022"),
        ("1985-12-31", "31.12.1985"),
        ("2001-01-01", "01.01.2001"),
    ],
)
def test_get_data_parametrized(iso_input: str, expected_output: str) -> None:
    assert get_data(iso_input) == expected_output
