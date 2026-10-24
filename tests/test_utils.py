import json
from unittest.mock import mock_open, patch

from src import utils


def test_data_json_with_open_mock():
    fake_data = [{"id": 1}, {"id": 2}]

    m = mock_open(read_data=json.dumps(fake_data))

    with patch("builtins.open", m):
        result = utils.data_json("fake_path.json")
    assert result == fake_data


def test_data_json_no_file():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = utils.data_json("fake_path.json")
    assert result == []


def test_data_json_decode_error():
    m = mock_open(read_data="{не json")

    with patch("builtins.open", m) as mock_data:
        result = utils.data_json("fake_path")
    assert result == []
    mock_data.assert_called_once_with("fake_path", encoding="utf-8")


def test_transaction_amount_rub():
    transactions = [{"operationAmount": {"amount": "31957.58", "currency": {"code": "RUB"}}}]

    result = {"amount_RUB": 31957.58, "amount_USD": 0, "amount_EUR": 0}
    assert utils.transaction_amount(transactions) == result


def test_transaction_amount_all():
    transactions = [
        {"operationAmount": {"amount": "100", "currency": {"code": "RUB"}}},
        {"operationAmount": {"amount": "50", "currency": {"code": "USD"}}},
        {"operationAmount": {"amount": "20", "currency": {"code": "EUR"}}},
    ]

    result = {"amount_RUB": 100, "amount_USD": 50, "amount_EUR": 20}
    assert utils.transaction_amount(transactions) == result


def test_transactions_amount_all_zero():
    transactions = [
        {"operationAmount": {"amount": "0", "currency": {"code": "RUB"}}},
        {"operationAmount": {"amount": "0", "currency": {"code": "USD"}}},
        {"operationAmount": {"amount": "0", "currency": {"code": "EUR"}}},
    ]

    result = {"amount_RUB": 0, "amount_USD": 0, "amount_EUR": 0}
    assert utils.transaction_amount(transactions) == result


def test_transactions_amount_incorrect_data():
    transaction = [{"operationAmount": {"amount": "abc", "currency": {"code": "EUR"}}}]

    result = {"amount_RUB": 0, "amount_USD": 0, "amount_EUR": 0}
    assert utils.transaction_amount(transaction) == result


def test_transaction_amount_no_operation_amount():
    transaction = [{"id": 1}]
    result = {"amount_RUB": 0, "amount_USD": 0, "amount_EUR": 0}
    assert utils.transaction_amount(transaction) == result


def test_transactions_amount_clean_list():
    transactions = []
    result = {"amount_RUB": 0, "amount_USD": 0, "amount_EUR": 0}
    assert utils.transaction_amount(transactions) == result


def test_data_json_with_real_file(tmp_path):
    file_path = tmp_path / "test.json"
    file_path.write_text(json.dumps([{"id": 1}, {"id": 2}], ensure_ascii=False), encoding="utf-8")

    result = utils.data_json(str(file_path))

    assert result == [{"id": 1}, {"id": 2}]
