import pytest
from project import check_budget_input, check_number_of_stocks, is_valid_date_format, check_valid_start_end_date, check_symbol_existence

# TypeError refers to a situation where something like a function is expecting to get one type as an argument, but it's given something else instead. For instance, it could be expecting a list, but given an integer.
# ValueError refers to a situation where the type of the aforementioned argument is okay, but the actual content doesn't match some agreed-upon rule.

def test_check_budget_input():
    assert check_budget_input(10000.2) == 10000.2
    assert check_budget_input(10000.0) == 10000.0
    assert check_budget_input(10000) == 10000
    with pytest.raises(TypeError):
        check_budget_input("abc")

def test_check_number_of_stocks():
    assert check_number_of_stocks(10) == 10
    with pytest.raises(TypeError):
        check_number_of_stocks("abc")
    with pytest.raises(TypeError):
        check_number_of_stocks("10.2")
    with pytest.raises(TypeError):
        check_number_of_stocks("10.0")

def test_is_valid_date_format():
    assert is_valid_date_format("2024-02-15") == "2024-02-15"
    with pytest.raises(ValueError):
        is_valid_date_format("abc")
    with pytest.raises(ValueError):
        is_valid_date_format("02/01/2023")
    with pytest.raises(ValueError):
        is_valid_date_format("2024-03-32")

def test_check_valid_start_end_date():
    assert check_valid_start_end_date("2024-02-01", "2024-02-15") == ("2024-02-01", "2024-02-15")
    with pytest.raises(ValueError):
        check_valid_start_end_date("2024-02-15", "2024-02-01")

def test_check_symbol_existence():
    assert check_symbol_existence("AAPL", "2024-02-01", "2024-02-15") == "AAPL"
    with pytest.raises(ValueError):
        ("FAKE", "2024-02-01", "2024-02-15")
