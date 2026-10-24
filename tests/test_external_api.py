from unittest.mock import patch, MagicMock

from requests import RequestException
from src import external_api


def test_transaction_rub():
    """Тест: проверка транзакции в рублях"""
    result = external_api.transaction({"operationAmount": {
      "amount": "1550.12",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }}})
    assert result == 1550.12


@patch("src.external_api.requests.get")
def test_transaction_usd(mock_requests):
    """Тест: транзакция в usd"""
    fake_requests = MagicMock()
    fake_requests.json.return_value = {"result": 80540.0}
    fake_requests.raise_for_status.return_value = None
    mock_requests.return_value = fake_requests

    result = external_api.transaction({"operationAmount": {
      "amount": "1000.0",
      "currency": {
        "name": "USD",
        "code": "USD"
      }}})
    assert result == 80540.0


def test_transaction_no_operation_amount():
    """Тест: отсутствия ключа operation_amount"""
    result = external_api.transaction({})
    assert result is None


@patch("src.external_api.requests.get")
def test_convert_to_rub_success(mock_requests):
    """Тест: успешный ответ от API"""
    fake_response = MagicMock()
    fake_response.json.return_value = {"result": 1550.12}
    fake_response.raise_for_status.return_value = None
    mock_requests.return_value = fake_response

    result = external_api._convert_to_rub(1550.12, "fake_currency")
    assert result == 1550.12


@patch("src.external_api.requests.get")
def test_convert_to_rub_error(mock_requests):
    """Тест: ошибка сети или API"""
    fake_response = MagicMock()
    fake_response.raise_for_status.side_effect = RequestException("500")
    mock_requests.return_value = fake_response
    result = external_api._convert_to_rub(13124.1, "fake_currency")
    assert result is None



# import json
# from unittest.mock import MagicMock, patch, mock_open
#
# import requests
# from requests import ConnectionError
#
# from src import external_api
#
#
# def test_transaction_return_rub():
#     """Тест: возвращает ли функция сумму в рублях"""
#     fake_data = {
#     "id": 441945886,
#     "state": "EXECUTED",
#     "date": "2019-08-26T10:50:58.294041",
#     "operationAmount": {
#       "amount": "31957.58",
#       "currency": {
#         "name": "руб.",
#         "code": "RUB"
#       }
#     },
#     "description": "Перевод организации",
#     "from": "Maestro 1596837868705199",
#     "to": "Счет 64686473678894779589"
#   }
#     m = mock_open(read_data=json.dumps(fake_data))
#
#     with patch("builtins.open", m):
#         result = external_api.transaction("fake_path")
#         assert result == "31957.58"
#
#
#
#
#
#
#

# def test_transaction_success():
#     """Тест: возвращает ли функция сумму в рублях"""
#     fake_response = MagicMock()
#     fake_response.json.return_value = {"result": 90.5}
#     fake_response.raise_for_status.return_value = None
#
#     with patch("src.external_api.requests.get", return_value=fake_response):
#         result = external_api.transaction({"from": "USD", "to": "RUB", "amount": 100})
#
#     assert result == 90.5


# def test_transaction_network_error():
#     """Тест: сетевая ошибка"""
#     with patch("src.external_api.requests.get", side_effect=ConnectionError("no net")):
#         result = external_api.transaction({"from": "USD", "to": "RUB", "amount": 100})
#
#     assert result is None
#
#
# def test_transaction_no_result():
#     """Тест: отсутствие значения на сайте"""
#     fake_response = MagicMock()
#     fake_response.json.return_value = {"error": "invalid payload"}
#     fake_response.raise_for_status.return_value = None
#
#     with patch("src.external_api.requests.get", return_value=fake_response):
#         result = external_api.transaction({"from": "USD", "to": "RUB", "amount": 100})
#
#     assert result is None
#
#
# def test_transaction_http_error():
#     """Тест: HTTP ошибка 401"""
#     fake_response = MagicMock()
#     fake_response.raise_for_status.side_effect = requests.HTTPError("401")
#
#     with patch("src.external_api.requests.get", return_value=fake_response):
#         result = external_api.transaction({"from": "USD", "to": "RUB", "amount": 100})
#
#     assert result is None
