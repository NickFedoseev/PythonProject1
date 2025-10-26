from unittest.mock import patch

from src.transaction_readers import read_transactions_from_csv, read_transactions_from_excel


@patch("src.transaction_readers.pd.read_csv")
def test_read_transactions_from_csv(mock_read_csv):
    mock_read_csv.return_value.to_dict.return_value = [{"id": 1, "amount": 100}]
    result = read_transactions_from_csv("fake.csv")
    assert result == [{"id": 1, "amount": 100}]
    mock_read_csv.assert_called_once_with("fake.csv", sep=";")


@patch("src.transaction_readers.pd.read_excel")
def test_read_transactions_from_excel(mock_read_excel):
    mock_read_excel.return_value.to_dict.return_value = [{"id": 2, "amount": 200}]
    result = read_transactions_from_excel("fake.xlsx")
    assert result == [{"id": 2, "amount": 200}]
    mock_read_excel.assert_called_once_with("fake.xlsx")
