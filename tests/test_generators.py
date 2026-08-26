from src.generators import filter_by_currency, transaction_descriptions, card_number_generator
import pytest
from typing import List, Dict, Any


def test_yields_amounts(transactions):
    result = list(transaction_descriptions(transactions))
    assert len(result) == len(transactions)
    # Проверяем, что возвращаются именно суммы, а не словари
    for amount in result:
        assert isinstance(amount, (int, float))

# def test_empty_list():
#     transactions: List[Dict[str, Any]] = []
#     result = list(transaction_descriptions(transactions))
#     assert result == []
#
# def test_single_transaction():
#     transactions = [{"operationAmount": 100}]
#     result = list(transaction_descriptions(transactions))
#     assert result == [100]
#
# def test_missing_key_raises():
#     transactions = [{}]
#     with pytest.raises(KeyError):
#         list(transaction_descriptions(transactions))
#
# def test_multiple_transactions():
#     transactions = [
#         {"operationAmount": 10},
#         {"operationAmount": 20},
#         {"operationAmount": 30},
#     ]
#     result = list(transaction_descriptions(transactions))
#     assert result == [10, 20, 30]


def test_card_number_generator():
    pass
