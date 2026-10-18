from unittest.mock import MagicMock, patch

import requests
from requests import ConnectionError

from src import external_api


def test_transaction_success():
    """Тест: верно ли работает функция"""
    fake_response = MagicMock()
    fake_response.json.return_value = {"result": 90.5}
    fake_response.raise_for_status.return_value = None

    with patch("src.external_api.requests.get", return_value=fake_response):
        result = external_api.transaction({"from": "USD", "to": "RUB", "amount": 100})

    assert result == 90.5


def test_transaction_network_error():
    """Тест: сетевая ошибка"""
    with patch("src.external_api.requests.get", side_effect=ConnectionError("no net")):
        result = external_api.transaction({"from": "USD", "to": "RUB", "amount": 100})

    assert result is None


def test_transaction_no_result():
    """Тест: отсутствие значения на сайте"""
    fake_response = MagicMock()
    fake_response.json.return_value = {"error": "invalid payload"}
    fake_response.raise_for_status.return_value = None

    with patch("src.external_api.requests.get", return_value=fake_response):
        result = external_api.transaction({"from": "USD", "to": "RUB", "amount": 100})

    assert result is None


def test_transaction_http_error():
    """Тест: HTTP ошибка 401"""
    fake_response = MagicMock()
    fake_response.raise_for_status.side_effect = requests.HTTPError("401")

    with patch("src.external_api.requests.get", return_value=fake_response):
        result = external_api.transaction({"from": "USD", "to": "RUB", "amount": 100})

    assert result is None
