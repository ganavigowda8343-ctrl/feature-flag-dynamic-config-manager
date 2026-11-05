"""
Hypothesis Property-Based Fuzz Testing Suite for Processor Application
Validates that functions never crash under arbitrary Unicode strings, None, or edge-case payloads.
"""
from hypothesis import given, strategies as st
from processor import parse_claim, age_average, payable_charge


@given(st.text() | st.none())
def test_parse_claim_no_crash(s):
    """Property: parse_claim should gracefully handle any text or None without crashing."""
    try:
        res = parse_claim(s)
        assert isinstance(res, tuple) and len(res) == 2
    except Exception as e:
        assert False, f"parse_claim crashed with: {e}"


@given(st.text() | st.none())
def test_age_average_no_crash(s):
    """Property: age_average should gracefully handle any CSV text or None without crashing."""
    try:
        res = age_average(s)
        assert isinstance(res, int)
    except Exception as e:
        assert False, f"age_average crashed with: {e}"


@given(st.text() | st.none())
def test_payable_charge_no_crash(s):
    """Property: payable_charge should gracefully handle any delimited text or None without crashing."""
    try:
        res = payable_charge(s)
        assert isinstance(res, (int, float))
    except Exception as e:
        assert False, f"payable_charge crashed with: {e}"


# --- Deterministic Functional Assertions for Standard/Valid Inputs ---

def test_parse_claim_valid():
    """Verify normal behavior on valid input."""
    assert parse_claim("standard:30") == ("Standard", 30.0)
    assert parse_claim("premium:12") == ("Premium", 12.0)


def test_age_average_valid():
    """Verify normal behavior on valid input."""
    assert age_average("12,24,36") == 24
    assert age_average("10, 20, 30") == 20


def test_payable_charge_valid():
    """Verify normal behavior on valid input."""
    assert payable_charge("1500|200") == 1570.0
    assert payable_charge("1000|0") == 1180.0
