import json
import pytest

def load_amounts(path):
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise ValueError("Expected a list")
    for amount in value:
        if type(amount) is not int or amount < 0:
            raise ValueError("Invalid amount")
    return value

@pytest.mark.parametrize("values", [[], [0], [10, 20]])
def test_round_trip(tmp_path, values):
    path = tmp_path / "amounts.json"
    path.write_text(json.dumps(values), encoding="utf-8")
    assert load_amounts(path) == values

def test_boolean_is_rejected(tmp_path):
    path = tmp_path / "amounts.json"
    path.write_text("[true]", encoding="utf-8")
    with pytest.raises(ValueError):
        load_amounts(path)
