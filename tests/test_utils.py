from unittest.mock import Mock
from src.utils import data_json, transaction_amount


# @pytest.fixture
# def fixture_data_json():
#     """Данные из JSON для utils"""
#     return [
#   {
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
#   },
#   {
#     "id": 41428829,
#     "state": "EXECUTED",
#     "date": "2019-07-03T18:35:29.512364",
#     "operationAmount": {
#       "amount": "8221.37",
#       "currency": {
#         "name": "USD",
#         "code": "USD"
#       }
#     },
#     "description": "Перевод организации",
#     "from": "MasterCard 7158300734726758",
#     "to": "Счет 35383033474447895560"
#   }]


# def test_data_json():
#     mock_data_json = Mock(return_value = [])
#     clean_list = mock_data_json
#     assert data_json(clean_list) == []
