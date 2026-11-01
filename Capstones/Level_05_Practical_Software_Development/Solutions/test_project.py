import json
import pytest
from project import load_amounts, summarize

@pytest.mark.parametrize("amounts,budget,expected", [([],0,0),([120,80],500,300),([120],100,-20)])
def test_remaining(amounts, budget, expected):
    original = amounts.copy()
    assert summarize(amounts, budget)["remaining"] == expected
    assert amounts == original

@pytest.mark.parametrize("text", ["not json", "[true]", "[-1]", "{}"])
def test_invalid_files(tmp_path, text):
    path = tmp_path / "amounts.json"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError):
        load_amounts(path)

def test_round_trip(tmp_path):
    path = tmp_path / "amounts.json"
    path.write_text(json.dumps([120,80]), encoding="utf-8")
    assert load_amounts(path) == [120,80]
