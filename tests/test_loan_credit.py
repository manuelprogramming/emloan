import pytest
from pathlib import Path
import json

import numpy as np
import pandas as pd

from emloan import loan


def test_annuity_from_period_basic():
    # 100,000 loan, 5% rate, 10 years
    result = loan.annuity_from_period(100000, 0.05, 10)
    assert isinstance(result, float)
    assert result > 0
    # Calculated manually: ~12950.46
    assert abs(result - 12950.46) < 1


def test_annuity_from_period_zero_period():
    # Should raise ZeroDivisionError or return inf/large value
    try:
        loan.annuity_from_period(100000, 0.05, 0)
        assert False, "Should raise ZeroDivisionError for zero period"
    except ZeroDivisionError:
        pass


def test_annuity_from_period_zero_loan():
    # Zero loan should return 0
    result = loan.annuity_from_period(0, 0.05, 10)
    assert result == 0


def test_annuity_from_period_negative_loan():
    # Negative loan should return negative annuity
    result = loan.annuity_from_period(-100000, 0.05, 10)
    assert result < 0
    # Should be negative of the positive case
    pos = loan.annuity_from_period(100000, 0.05, 10)
    assert abs(result + pos) < 1


def test_loan_period_valid():
    # Test with valid data
    loan_amount = 100000
    annuity = 6000
    interest_rate = 0.05
    result = loan.loan_period(loan_amount, annuity, interest_rate)

    # Calculate expected manually
    expected = np.log(1 - (interest_rate * loan_amount / annuity)) / np.log(
        1 / (1 + interest_rate)
    )

    assert np.isclose(result, expected, rtol=1e-6)


def test_loan_period_exact_limit():
    # Annuity is exactly equal to interest_rate * loan_amount -> should raise ValueError
    loan_amount = 100000
    interest_rate = 0.05
    annuity = interest_rate * loan_amount  # exactly the threshold

    with pytest.raises(ValueError, match="annuity must be greater"):
        loan.loan_period(loan_amount, annuity, interest_rate)


def test_loan_period_below_limit():
    # Annuity is less than interest_rate * loan_amount -> should raise ValueError
    loan_amount = 100000
    interest_rate = 0.05
    annuity = interest_rate * loan_amount - 1  # slightly below the threshold

    with pytest.raises(ValueError, match="annuity must be greater"):
        loan.loan_period(loan_amount, annuity, interest_rate)


def test_loan_period_large_numbers():
    loan_amount = 1_000_000
    annuity = 120_000
    interest_rate = 0.07
    result = loan.loan_period(loan_amount, annuity, interest_rate)

    expected = np.log(1 - (interest_rate * loan_amount / annuity)) / np.log(
        1 / (1 + interest_rate)
    )
    assert np.isclose(result, expected, rtol=1e-6)


def test_loan_period_small_interest_rate():
    loan_amount = 100000
    annuity = 10000
    interest_rate = 0.0001
    result = loan.loan_period(loan_amount, annuity, interest_rate)

    expected = np.log(1 - (interest_rate * loan_amount / annuity)) / np.log(
        1 / (1 + interest_rate)
    )
    assert np.isclose(result, expected, rtol=1e-6)


def test_annuity_standard_values():
    loan_amount = 100000
    interest_rate = 0.05
    repayment_rate = 0.01

    result = loan.annuity_from_repayment_rate(
        loan_amount, interest_rate, repayment_rate
    )
    expected = round((loan_amount * repayment_rate) + loan_amount * interest_rate)

    assert np.isclose(result, expected)


def test_annuity_default_repayment_rate():
    loan_amount = 100000
    interest_rate = 0.04  # repayment_rate should default to 0.01

    result = loan.annuity_from_repayment_rate(loan_amount, interest_rate)
    expected = round((loan_amount * 0.01) + loan_amount * interest_rate)

    assert np.isclose(result, expected)


def test_annuity_zero_interest_rate():
    loan_amount = 50000
    interest_rate = 0.0
    repayment_rate = 0.02

    result = loan.annuity_from_repayment_rate(
        loan_amount, interest_rate, repayment_rate
    )
    expected = round((loan_amount * repayment_rate) + loan_amount * interest_rate)

    assert np.isclose(result, expected)


def test_annuity_zero_repayment_rate():
    loan_amount = 75000
    interest_rate = 0.03
    repayment_rate = 0.0

    result = loan.annuity_from_repayment_rate(
        loan_amount, interest_rate, repayment_rate
    )
    expected = round((loan_amount * repayment_rate) + loan_amount * interest_rate)

    assert np.isclose(result, expected)


def test_annuity_high_values():
    loan_amount = 10_000_000
    interest_rate = 0.08
    repayment_rate = 0.05

    result = loan.annuity_from_repayment_rate(
        loan_amount, interest_rate, repayment_rate
    )
    expected = round((loan_amount * repayment_rate) + loan_amount * interest_rate)

    assert np.isclose(result, expected)


def test_repayment_rate_standard_values():
    loan_amount = 100000
    interest_rate = 0.05
    annuity = 6000

    result = loan.repayment_rate_from_annuity(loan_amount, interest_rate, annuity)
    expected = annuity / loan_amount - interest_rate

    assert np.isclose(result, expected)


def test_repayment_rate_zero_interest_rate():
    loan_amount = 100000
    interest_rate = 0.0  # Zero credit rate
    annuity = 6000

    result = loan.repayment_rate_from_annuity(loan_amount, interest_rate, annuity)
    expected = annuity / loan_amount - interest_rate

    assert np.isclose(result, expected)


def test_repayment_rate_zero_annuity():
    loan_amount = 100000
    interest_rate = 0.05
    annuity = 0.0  # Zero annuity

    result = loan.repayment_rate_from_annuity(loan_amount, interest_rate, annuity)
    expected = annuity / loan_amount - interest_rate

    assert np.isclose(result, expected)


def test_repayment_rate_large_values():
    loan_amount = 1_000_000
    interest_rate = 0.07
    annuity = 150000

    result = loan.repayment_rate_from_annuity(loan_amount, interest_rate, annuity)
    expected = annuity / loan_amount - interest_rate

    assert np.isclose(result, expected)


def test_repayment_rate_edge_case_zero_loan_amount():
    loan_amount = 0.0  # Should raise an exception due to division by zero
    interest_rate = 0.05
    annuity = 5000

    with pytest.raises(ZeroDivisionError):
        loan.repayment_rate_from_annuity(loan_amount, interest_rate, annuity)


def test_repayment_rate_large_difference():
    loan_amount = 100000
    interest_rate = 0.03
    annuity = 120000

    result = loan.repayment_rate_from_annuity(loan_amount, interest_rate, annuity)
    expected = annuity / loan_amount - interest_rate

    assert np.isclose(result, expected)


def test_rest_dept_basic_functionality():
    # Test with typical loan, interest_rate, and annuity
    loan_amount = 100000
    interest_rate = 0.05  # 5% annual rate
    period = 10  # 10 periods (e.g., years)
    annuity = 15000

    result = loan.rest_dept(loan_amount, interest_rate, period, annuity)

    # Check that the result is a float value (final loan balance)
    assert isinstance(result, float)
    assert (
        result < loan_amount
    )  # Remaining loan balance should be less than initial loan amount


def test_rest_dept_hist_return():
    # Test with hist=True to get the detailed history
    loan_amount = 100000
    interest_rate = 0.05  # 5% annual rate
    period = 10  # 10 periods (e.g., years)
    annuity = 15000

    result = loan.rest_dept(loan_amount, interest_rate, period, annuity, hist=True)

    # Check that the result is a DataFrame
    assert isinstance(result, pd.DataFrame)
    assert result.shape[0] == period  # There should be 'period' rows in the DataFrame
    assert all(
        col in result.columns
        for col in ["Period", "Credit Pre", "Interest", "Repay", "Credit Post"]
    )


def test_zero_period():
    # Test with period = 0
    loan_amount = 100000
    interest_rate = 0.05
    period = 0
    annuity = 15000

    result = loan.rest_dept(loan_amount, interest_rate, period, annuity)
    assert result == loan_amount  # If no periods, loan balance should remain the same


def test_zero_loan_amount():
    # Test with loan amount = 0 (should remain 0 throughout)
    loan_amount = 0
    interest_rate = 0.05
    period = 10
    annuity = 15000

    result = loan.rest_dept(loan_amount, interest_rate, period, annuity)
    assert result == 0  # No loan amount should result in zero balance


def test_zero_annuity():
    # Test with annuity = 0 (interest will accumulate but no repayment)
    loan_amount = 100000
    interest_rate = 0.05
    period = 5
    annuity = 0  # No repayment

    result = loan.rest_dept(loan_amount, interest_rate, period, annuity)
    assert (
        result > loan_amount
    )  # Since no repayment, the balance will grow due to interest


def test_single_period_full_payment():
    # Test with period = 1 where the loan is fully paid off
    loan_amount = 100000
    interest_rate = 0.05
    period = 1  # Single period
    annuity = 100000  # Full payment in one period

    result = loan.rest_dept(loan_amount, interest_rate, period, annuity)
    assert result == loan_amount * interest_rate  # The loan should be fully paid off


def test_large_period_and_small_repayment():
    # Test with a large period and small repayments
    loan_amount = 100000
    interest_rate = 0.05
    period = 100  # 100 periods (e.g., years)
    annuity = 2000  # Small repayment amount

    result = loan.rest_dept(loan_amount, interest_rate, period, annuity)
    assert (
        result > 0
    )  # Loan balance will be slowly reduced, but not likely to be fully paid off


def test_negative_interest_rate():
    # Test with a negative credit rate
    loan_amount = 100000
    interest_rate = -0.05  # Negative interest rate
    period = 10
    annuity = 15000

    with pytest.raises(ValueError):
        loan.rest_dept(loan_amount, interest_rate, period, annuity)


def test_rounding_behavior():
    # Test that credit post is rounded to two decimal places
    loan_amount = 100000
    interest_rate = 0.05
    period = 5
    annuity = 15000

    result = loan.rest_dept(loan_amount, interest_rate, period, annuity, hist=True)
    assert all(
        result["Credit Post"].apply(lambda x: len(str(x).split(".")[-1]) <= 2)
    )  # Ensure rounding to 2 decimals


def test_large_loan_and_annuity():
    # Test with a very large loan and annuity
    loan_amount = 1e9  # 1 billion
    interest_rate = 0.05
    period = 30
    annuity = 1 + interest_rate * loan_amount  # Large annuity

    result = loan.rest_dept(loan_amount, interest_rate, period, annuity)
    assert (
        result < loan_amount
    )  # Remaining balance should be less than initial loan amount after 30 periods
