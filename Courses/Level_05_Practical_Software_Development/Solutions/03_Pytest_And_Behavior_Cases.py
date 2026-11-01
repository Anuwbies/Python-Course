import pytest

def parse_amount(text):
    amount = int(text)
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    return amount

def test_normal_amount():
    assert parse_amount("25") == 25

def test_zero_amount():
    assert parse_amount("0") == 0

def test_negative_amount_is_rejected():
    with pytest.raises(ValueError):
        parse_amount("-1")
