import pytest
from src.masks import get_mask_account, get_mask_card_number

# Фикстура для создания тестовых данных карт
@pytest.fixture(params=[
    ("7000792289606361", "7000 79** **** 6361"),  # корректный номер
    ("79289606361", "Номер карты должен содержать 16 символов"),  # короткий номер
    ("7000792896063610000", "Номер карты должен содержать 16 символов"),  # длинный номер
    ("70007928960636ы", "Номер карты должен содержать только цифры!"),  # символы
    ("", "Номер карты должен содержать только цифры!"),  # пустая строка
])
def card_test_data(request):
    return request.param

# Фикстура для создания тестовых данных счетов
@pytest.fixture(params=[
    ("73654108430135874305", "**4305"),  # корректный счет
    ("7365410843013587430a", "Номер счета должен содержать только цифры!"),  # символы
    ("", "Номер счета должен содержать только цифры!"),  # пустая строка
    ("736", "Номер счета должен содержать больше 4 символов"),  # короткий номер
])
def account_test_data(request):
    return request.param

# Переписанный тест с использованием фикстур
def test_get_mask_card_number(card_test_data):
    """Тестирование правильности маскирования номера карты."""
    input_data, expected = card_test_data
    assert get_mask_card_number(input_data) == expected

def test_get_mask_account(account_test_data):
    """Тестирование правильности маскирования банковского счета"""
    input_data, expected = account_test_data
    assert get_mask_account(input_data) == expected
