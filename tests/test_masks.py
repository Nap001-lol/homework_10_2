import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_mask_card_number():
    """Тест существующей карты"""
    result = get_mask_card_number("7000792289606361")
    assert result == "7000 79** **** 6361"
    assert isinstance(result, str)
    assert result.count("*") == 6
    assert len(result) == 19


@pytest.mark.parametrize("card_number", ["7000", "412357862394619234691238"])
def test_card_number_wrong_length(card_number):
    """Тест: неверная длина номера карты"""
    with pytest.raises(ValueError):
        get_mask_card_number(card_number)


@pytest.mark.parametrize("card_number", ["700079228960636s", "fasdfa"])
def test_card_number_not_digits(card_number):
    """Тест: номер карты содержит не только цифры"""
    with pytest.raises(ValueError):
        get_mask_card_number(card_number)


def test_card_number_empty_string():
    """Тест: введена пустая строка"""
    with pytest.raises(ValueError):
        get_mask_card_number("")


def test_mask_card_account():
    """Тест существующего аккаунта"""
    result = get_mask_account("73654108430135874305")

    assert result == "**4305"
    assert isinstance(result, str)
    assert result.count("*") == 2
    assert len(result) == 6


@pytest.mark.parametrize("card_account", ["123", "001"])
def test_card_account_wrong_length(card_account):
    """Тест: неверная длина номера карты"""
    with pytest.raises(ValueError):
        get_mask_account(card_account)


@pytest.mark.parametrize("card_account", ["dsasg", "2314213f13214122"])
def test_card_account_not_digits(card_account):
    """Тест: номер счета содержит не только цифры"""
    with pytest.raises(ValueError):
        get_mask_account(card_account)


def test_card_account_empty_strings():
    """Тест: введена пустая строка"""
    with pytest.raises(ValueError):
        get_mask_account("")
