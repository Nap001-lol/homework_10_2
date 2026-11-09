from unittest.mock import patch

import pandas as pd

from src.dataframe import df_transactions_csv, df_transactions_xlsx


@patch("src.dataframe.pd.read_csv")
def test_df_transactions_csv(mock_read_csv):
    """Тест: успешное чтение csv"""
    fake_df = pd.DataFrame({"id": [1], "amount": [100]})
    mock_read_csv.return_value = fake_df

    result = df_transactions_csv("fake_path.csv")

    assert result == [{"id": 1, "amount": 100}]
    mock_read_csv.assert_called_once_with("fake_path.csv")


@patch("src.dataframe.pd.read_excel")
def test_df_transactions_xlsx(mock_read_xlsx):
    """Тест: успешное чтение excel"""
    fake_df = pd.DataFrame({"id": [1], "amount": [100]})
    mock_read_xlsx.return_value = fake_df

    result = df_transactions_xlsx("fake_path.xlsx")

    assert result == [{"id": 1, "amount": 100}]
    mock_read_xlsx.assert_called_once_with("fake_path.xlsx")


def test_df_transactions_csv_not_found():
    result = df_transactions_csv("несуществующий_файл.csv")
    assert result == []


@patch("src.dataframe.pd.read_csv")
def test_df_transactions_csv_error_f(mock_read_csv):
    """Тест: отсутствие файла csv"""
    mock_read_csv.side_effect = FileNotFoundError

    result = df_transactions_csv("fake_path.csv")

    assert result == []
    mock_read_csv.assert_called_once_with("fake_path.csv")


@patch("src.dataframe.pd.read_excel")
def test_df_transactions_xlsx_error_f(mock_read_xlsx):
    """Тест: отсутствие файла excel"""
    mock_read_xlsx.side_effect = FileNotFoundError

    result = df_transactions_xlsx("fake_path.xlsx")

    assert result == []
    mock_read_xlsx.assert_called_once_with("fake_path.xlsx")


@patch("src.dataframe.pd.read_csv")
def test_df_transactions_csv_error_e(mock_read_csv):
    """Тест: ошибка чтения файла csv"""
    mock_read_csv.side_effect = Exception

    result = df_transactions_csv("fake_path.csv")

    assert result == []
    mock_read_csv.assert_called_once_with("fake_path.csv")


@patch("src.dataframe.pd.read_excel")
def test_df_transactions_xlsx_error_e(mock_read_xlsx):
    """Тест: ошибка чтения файла excel"""
    mock_read_xlsx.side_effect = Exception

    result = df_transactions_xlsx("fake_path.xlsx")

    assert result == []
    mock_read_xlsx.assert_called_once_with("fake_path.xlsx")
