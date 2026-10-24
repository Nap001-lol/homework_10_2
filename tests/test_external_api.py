from unittest.mock import MagicMock, patch

from requests import RequestException

from src import external_api


def test_transaction_rub():
    """Тест: проверка транзакции в рублях"""
    result = external_api.transaction(
        {"operationAmount": {"amount": "1550.12", "currency": {"name": "руб.", "code": "RUB"}}}
    )
    assert result == 1550.12


@patch("src.external_api.requests.get")
def test_transaction_usd(mock_requests):
    """Тест: транзакция в usd"""
    fake_requests = MagicMock()
    fake_requests.json.return_value = {"result": 80540.0}
    fake_requests.raise_for_status.return_value = None
    mock_requests.return_value = fake_requests

    result = external_api.transaction(
        {"operationAmount": {"amount": "1000.0", "currency": {"name": "USD", "code": "USD"}}}
    )
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
