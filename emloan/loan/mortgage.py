from dataclasses import dataclass, field

import numpy as np
import pandas as pd


from . import credit


@dataclass
class Mortgage:
    amount: float 
    interest_rate: float
    _annuity: float
    _period: int = 10
    _repayment_rate: float = 1.5

    @property
    def annuity(self):
        return self._annuity
    
    @property
    def period(self):
        return self._period

    @property
    def repayment_rate(self):
        return self._repayment_rate

    @property
    def repay_time_total(self) -> int:
        return int(np.round(credit.loan_period(self.amount, annuity=self.annuity, interest_rate=self.interest_rate)))

    def credit_costs(self) -> float:
        return credit.rest_dept(self.amount, self.interest_rate, self.repay_time_total, self.annuity, hist=True)["Interest"]

    def credit_cost_mean(self) -> float:
        return credit.rest_dept(self.amount, self.interest_rate, self.repay_time_total, self.annuity, hist=True)["Interest"].mean()

    def outlook(self) -> pd.DataFrame:
        return credit.rest_dept(self.amount, self.interest_rate, self.repay_time_total, self.annuity, hist=True)

    def outlook_plot(self):
        return credit.plot_credit_repay_hist(self.outlook())

    def rest_dept_by_period(self, period: float):
        return credit.rest_dept(self.amount, self.interest_rate, period, self.annuity)

    def update_annuity(self, annuity: float) -> None:
        self._annuity = annuity
        self._repayment_rate = credit.repayment_rate_from_annuity(
            self.amount, self.interest_rate, self.annuity)

    def update_repayment_rate(self, repayment_rate: float) -> None:
        self._repayment_rate = repayment_rate
        self._annuity = credit.annuity_from_repayment_rate(
            self.amount, self.interest_rate, self.repayment_rate)

    def update_interest_rate(self, interest_rate: float) -> None:
        self.interest_rate = interest_rate

    def update_repay_time(self, repay_time: float) -> None:
        self._annuity = credit.annuity_from_period(
            self.amount, self.interest_rate, repay_time)
        self._repayment_rate = credit.repayment_rate_from_annuity(
            self.amount, self.interest_rate, self.annuity)

    def summary(self) -> pd.DataFrame:
        return pd.DataFrame(
            data=[
                self.interest_rate,
                self.repayment_rate,
                self.annuity,
                self.repay_time_total
            ],
            index=[
                "Credit Rate",
                "Initial Repayment Rage"
                "Annuity",
                "Repay Time Total"
            ]
        )

    def summary_dict(self):
        return {
            "Interest Rate": self.interest_rate,
            "Initial Repayment Rate": self.repayment_rate,
            "Annuity": self.annuity,
            "Repay Time Total": self.repay_time_total
        }
