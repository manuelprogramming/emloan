from . import calculators
from . import immo


prop_data = {
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


def start_immo() -> immo.Immo:
    interest_rate = 0.0325
    period = 25

    return calculators.calc_property_by_period(prop_data, interest_rate, period)
