import pytest

from emloan import immo


@pytest.fixture
def default_cashflow():
    return immo.CashFlow(
        net_cold_rent=1000, operating_expenses=400, operating_income=300
    )


def test_default_values(default_cashflow: immo.CashFlow):
    net_cold_rent = 1000
    operating_expenses = 400
    operating_income = 300

    assert default_cashflow.net_cold_rent == net_cold_rent
    assert default_cashflow.operating_expenses == operating_expenses
    assert default_cashflow.operating_income == operating_income
    assert default_cashflow.net_operating_cost == operating_expenses - operating_income
    assert default_cashflow.total_annually == 12 * (net_cold_rent + operating_income)
    assert default_cashflow.net == net_cold_rent + operating_income - operating_expenses
    assert default_cashflow.net_annually == 12 * (
        net_cold_rent + operating_income - operating_expenses
    )


@pytest.mark.parametrize("net_cold_rent", [-100, 0, 100, 300, 1e8])
def test_set_net_cold_rent(default_cashflow: immo.CashFlow, net_cold_rent: float):
    default_cashflow.set_net_cold_rent(net_cold_rent)
    if net_cold_rent < 0:
        assert default_cashflow.net_cold_rent == 0
    else:
        assert default_cashflow.net_cold_rent == net_cold_rent


@pytest.mark.parametrize("operating_income", [-100, 0, 100, 300, 1e8])
def test_set_operating_income(default_cashflow: immo.CashFlow, operating_income: float):
    default_cashflow.set_operating_income(operating_income)
    if operating_income < 0:
        assert default_cashflow.operating_income == 0
    else:
        assert default_cashflow.operating_income == operating_income


@pytest.mark.parametrize("operating_income", [-100, 0, 100, 300, 1e8])
def test_set_operating_income(default_cashflow: immo.CashFlow, operating_income: float):
    default_cashflow.set_operating_income(operating_income)
    if operating_income < 0:
        assert default_cashflow.operating_income == 0
    else:
        assert default_cashflow.operating_income == operating_income


@pytest.mark.parametrize("operating_expenses", [-100, 0, 100, 300, 1e8])
def test_set_operating_income(
    default_cashflow: immo.CashFlow, operating_expenses: float
):
    default_cashflow.set_operating_expenses(operating_expenses)
    if operating_expenses < 0:
        assert default_cashflow.operating_expenses == 0
    else:
        assert default_cashflow.operating_expenses == operating_expenses
