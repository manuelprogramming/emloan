import pytest

from emloan import calculators

house_props = {
    "details": {"living_space": 100},
    "base_cost": {
        "price": 375000,
        "notary_rate": 0.015,
        "property_buy_tax_rate": 0.05,
        "land_registry_rate": 0.005,
        "agent_rate": 0.0357,
        "proprietary_capital_rate": 0.2,
        "loan_rate": 0.8,
    },
    "cash_flow": {
        "period": "monthly",
        "net_cold_rent": 1030,
        "operating_expanses": 250,
        "operating_income": 200,
    },
}


@pytest.mark.parametrize(
    ("interest_rate", "repayment_rate"),
    [(0.01, 0.02), (0.013, 0.03), (0.024 / 3, 0.05)],
)
def test_calc_property_by_repayment_rate(interest_rate: float, repayment_rate: float):
    immo = calculators.calc_property_by_repayment_rate(house_props, interest_rate, repayment_rate)
    assert immo.mortgage.interest_rate == interest_rate
    assert immo.mortgage.repayment_rate == repayment_rate
    
