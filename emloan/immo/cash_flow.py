import logging
from dataclasses import dataclass
from typing import Literal

import pandas as pd

log = logging.getLogger(__name__)


@dataclass
class CashFlow:
    net_cold_rent: float
    operating_expenses: float
    operating_income: float

    @property
    def net_operating_cost(self) -> float:
        return self.operating_expenses - self.operating_income

    @property
    def total_annually(self) -> float:
        return 12 * (self.net_cold_rent + self.operating_income)

    @property
    def net(self) -> float:
        return self.net_cold_rent - self.net_operating_cost

    @property
    def net_annually(self) -> float:
        return 12 * self.net

    def set_net_cold_rent(self, value: float) -> None:
        if value < 0:
            value = 0
            log.info("Net cold rent cannot be negative and was set 0")
        self.net_cold_rent = value

    def set_operating_income(self, value: float) -> None:
        if value < 0:
            value = 0
            log.info("Operating income cannot be negative and was set 0")
        self.operating_income = value

    def set_operating_expenses(self, value: float) -> None:
        if value < 0:
            value = 0
            log.info("Operating income cannot be negative and was set 0")
        self.operating_expenses = value

    def summary(self, annuity: float = 0) -> pd.DataFrame:
        _summary = pd.DataFrame(
            data={
                "Monthly": [
                    self.net_cold_rent,
                    -self.net_operating_cost,
                    self.operating_income,
                    -self.operating_expenses,
                    round(-annuity / 12, 2),
                    round(self.net - annuity / 12, 2),
                ],
                "Annually": [
                    self.net_cold_rent * 12,
                    -self.net_operating_cost * 12,
                    self.operating_income * 12,
                    -self.operating_expenses * 12,
                    round(-annuity, 2),
                    round(self.net_annually - annuity, 2),
                ],
            },
            index=[
                "Net Cold Rent",
                "Net Operating Cost",
                "Operating Income",
                "Operating Expenses",
                "Annuity",
                "Total",
            ],
        )

        if annuity == 0:
            _summary = _summary.drop(["Annuity"])
        return _summary


def get_cashflow(
    period: Literal["monthly", "annually"] = "monthly",
    net_cold_rent: float = 0,
    operating_expanses: float = 0,
    operating_income: float = None,
) -> CashFlow:
    if period == "monthly":
        return CashFlow(
            net_cold_rent=net_cold_rent,
            operating_expenses=operating_expanses,
            operating_income=operating_income,
        )
    if period == "annually":
        return CashFlow(
            net_cold_rent=12 * net_cold_rent,
            operating_expenses=12 * operating_expanses,
            operating_income=12 * operating_income,
        )
