from dataclasses import dataclass
import pandas as pd

from .. import loan
from . import CashFlow, BaseCost


@dataclass
class Scenario:
    appreciation: float
    inflation: float

    def to_tuple(self):
        return self.appreciation, self.inflation


def get_default() -> dict[str, Scenario]:
    return {
        "good": Scenario(0.02, 0.01),
        "medium": Scenario(0.02, 0.02),
        "bad": Scenario(0.02, 0.03),
    }


def scenarios_to_dict(
    cap_dev_scenarios: dict[str, Scenario],
) -> dict[str, tuple[float]]:
    return {name: scenario.to_tuple() for name, scenario in cap_dev_scenarios.items()}


def capital_development(
    mortgage: loan.Mortgage,
    cash_flow: CashFlow,
    base_cost: BaseCost,
    scenarios: dict[str, Scenario],
):
    scenarios_df = pd.DataFrame()
    scenarios_df["Period"] = mortgage.outlook()["Period"]

    for name, scenario in scenarios.items():
        price_outlook = loan.compound_interest_detailed(
            base_cost.value(),
            loan.real_rate(scenario.appreciation, scenario.inflation),
            mortgage.repay_time_total,
        )["Total"]
        amount = (
            price_outlook
            - mortgage.outlook()["Credit Post"]
            + loan.compound_interest_detailed(
                0,
                -scenario.inflation,
                mortgage.repay_time_total,
                cash_flow.net_annually_minus_annuity(mortgage.annuity),
            )["Total"]
        )
        scenarios_df[name] = amount
        scenarios_df[f"{name} Annualized Return"] = loan.annualized_rate(
            end_capital=amount,
            starting_capital=base_cost.proprietary_capital,
            period=pd.Series(scenarios_df["Period"]),
        )

    return scenarios_df
