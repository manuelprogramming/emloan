import numpy as np
import pandas as pd

from . import loan
from . import immo


def calc_property_by_repayment_rate(
    prop_data: dict, interest_rate: float, repayment_rate: float
) -> immo.Immo:
    """
    Calculate the property object from the property data and the credit and repay rates.
    """
    # get the details
    details = immo.Details(**prop_data["details"])

    # get the base cost
    base_cost = immo.BaseCost(**prop_data["base_cost"])

    # get the cash flow
    cash_flow = immo.get_cashflow(**prop_data["cash_flow"])

    # get the annuity
    annuity = loan.annuity_from_repayment_rate(
        loan_amount=base_cost.loan,
        interest_rate=interest_rate,
        repayment_rate=repayment_rate,
    )

    period = loan.loan_period(
        loan_amount=base_cost.loan, annuity=annuity, interest_rate=interest_rate
    )

    mortgage = loan.Mortgage(
        base_cost.loan,
        _annuity=annuity,
        interest_rate=interest_rate,
        _period=int(np.round(period)),
        _repayment_rate=repayment_rate,
    )

    temp_immo = immo.Immo(
        details=details,
        base_cost=base_cost,
        cash_flow=cash_flow,
        mortgage=mortgage,
        tax_rates=immo.TaxRates(),
    )

    return temp_immo


def calc_property_by_annuity(
    prop_data: dict, interest_rate: float, annuity: float
) -> immo.Immo:
    """
    Calculate the property object from the property data and the credit and repay rates.
    """
    # get the details
    details = immo.Details(**prop_data["details"])

    # get the base cost
    base_cost = immo.BaseCost(**prop_data["base_cost"])

    # get the cash flow
    cash_flow = immo.get_cashflow(**prop_data["cash_flow"])

    # get the repay rate
    repayment_rate = loan.repayment_rate_from_annuity(
        loan_amount=base_cost.loan, interest_rate=interest_rate, annuity=annuity
    )

    period = loan.loan_period(
        loan_amount=base_cost.loan, annuity=annuity, interest_rate=interest_rate
    )

    mortgage = loan.Mortgage(
        base_cost.loan,
        _annuity=annuity,
        interest_rate=interest_rate,
        _period=int(np.round(period)),
        _repayment_rate=repayment_rate,
    )

    temp_immo = immo.Immo(
        details=details,
        base_cost=base_cost,
        cash_flow=cash_flow,
        mortgage=mortgage,
        tax_rates=immo.TaxRates(),
    )

    return temp_immo


def calc_property_by_period(
    prop_data: dict, interest_rate: float, period: float
) -> immo.Immo:
    """
    Calculate the property object from the property data and the credit and repay rates.
    """
    # get the details
    details = immo.Details(**prop_data["details"])

    # get the base cost
    base_cost = immo.BaseCost(**prop_data["base_cost"])

    # get the cash flow
    # prop_data["cash_flow"]["monthly_maintenance_net"] = running_cost.monthly_maintenance_net
    cash_flow = immo.get_cashflow(**prop_data["cash_flow"])

    # get the annuity
    annuity = loan.annuity_from_period(
        loan_amount=base_cost.loan, interest_rate=interest_rate, period=period
    )

    repayment_rate = loan.repayment_rate_from_annuity(
        loan_amount=base_cost.loan, interest_rate=interest_rate, annuity=annuity
    )

    mortgage = loan.Mortgage(
        base_cost.loan,
        _annuity=annuity,
        interest_rate=interest_rate,
        _period=int(np.round(period)),
        _repayment_rate=repayment_rate,
    )

    temp_immo = immo.Immo(
        details=details,
        base_cost=base_cost,
        cash_flow=cash_flow,
        mortgage=mortgage,
        tax_rates=immo.TaxRates(),
    )

    return temp_immo
