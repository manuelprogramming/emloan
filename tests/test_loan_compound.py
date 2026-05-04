import numpy as np
import pandas as pd
import pytest

def annualized_rate(end_capital, starting_capital, period):
    return (end_capital / starting_capital) ** (1 / period) - 1

@pytest.mark.parametrize(
    "end_capital, starting_capital, period, expected",
    [
        pytest.param(121.0, 100.0, 2.0, 0.1, id="scalar_case"),
    ],
)
def test_annualized_rate_scalar_input(end_capital, starting_capital, period, expected):
    assert annualized_rate(end_capital, starting_capital, period) == pytest.approx(expected)

@pytest.mark.parametrize(
    "end_capital, starting_capital, period, expected",
    [
        pytest.param(np.array([121.0, 144.0]), 100.0, np.array([2.0, 2.0]), np.array([0.1, 0.2]), id="numpy_array_case"),
    ],
)
def test_annualized_rate_numpy_input(end_capital, starting_capital, period, expected):
    assert np.allclose(annualized_rate(end_capital, starting_capital, period), expected)

@pytest.mark.parametrize(
    "end_capital, starting_capital, period, expected",
    [
        pytest.param(pd.Series([121.0, 144.0]), 100.0, pd.Series([2.0, 2.0]), pd.Series([0.1, 0.2]), id="pandas_series_case"),
    ],
)
def test_annualized_rate_pandas_input(end_capital, starting_capital, period, expected):
    pd.testing.assert_series_equal(annualized_rate(end_capital, starting_capital, period), expected, atol=1e-7)

@pytest.mark.parametrize(
    "end_capital, starting_capital, period, expected",
    [
        pytest.param(np.array([110.0, 121.0]), 100.0, 1.0, np.array([0.1, 0.21]), id="mixed_input_case"),
    ],
)
def test_annualized_rate_mixed_input(end_capital, starting_capital, period, expected):
    assert np.allclose(annualized_rate(end_capital, starting_capital, period), expected)   