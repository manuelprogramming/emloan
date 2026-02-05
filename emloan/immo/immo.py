from dataclasses import dataclass
from typing import Self
import pandas as pd
import pickle

from . import costs
from . import cash_flow
from .. import loan
from . import details


@dataclass
class TaxRates:
    personal: float = 0.35
    depreciation: float = 0.02  # Abschreibung


@dataclass
class Immo:
    details: details.Details
    base_cost: costs.BaseCost
    cash_flow: cash_flow.CashFlow
    mortgage: loan.Mortgage
    tax_rates: TaxRates

    def total_taxes(self):
        """total amount of taxes"""
        return self.tax_rates.personal * (
            self.cash_flow.net_cold_rent
            - self.mortgage.credit_costs()
            - self.cash_flow.net_operating_cost
        )

    @property
    def return_on_equity(self) -> float:
        """return on equity"""
        if self.base_cost.proprietary_capital == 0:
            return 0
        return self.cash_flow.net_annually / self.base_cost.proprietary_capital

    @property
    def gross_rental_yield(self) -> float:
        """yield before cost: Bruttomietrendite"""
        return self.cash_flow.net_cold_rent * 12 / self.base_cost.total

    @property
    def net_rental_yield(self) -> float:
        """yield after subtracting all cost"""
        return (
            self.cash_flow.net_annually - self.mortgage.annuity
        ) / self.base_cost.total

    @property
    def multiplication_factor(self) -> int:
        """How much periods you need to pay back the house"""
        return int(self.base_cost.total // self.cash_flow.net_annually)

    def ten_year_net_capital_gain(self) -> int:
        """how much money you get gross out"""
        #if self.cash_flow.net_annually - self.mortgage.annuity <= 0:
        period = 10 if self.mortgage.period >= 10 else self.mortgage.period
        return round(
            self.base_cost.price
            + self.base_cost.modernisation
            - self.base_cost.proprietary_capital
            - self.mortgage.rest_dept_by_period(period),
            2,
        ) + period * (self.cash_flow.net_annually - self.mortgage.annuity)


    def ten_year_roe(self) -> float:
        if self.base_cost.proprietary_capital == 0:
            return 0
        return (
            (self.ten_year_net_capital_gain() + self.base_cost.proprietary_capital)
            / self.base_cost.proprietary_capital
        ) - 1

    @property
    def price_per_sqm(self) -> float:
        return self.base_cost.price / self.details.living_space

    @property
    def rent_per_sqm(self) -> float:
        return self.cash_flow.net_cold_rent / self.details.living_space

    def cost_effectiveness(self) -> dict:
        return {
            "Living Space": self.details.living_space,
            "Price/sqm": self.price_per_sqm,
            "Net Cold Rent/sqm": self.rent_per_sqm,
        }

    def eval(self) -> pd.DataFrame:
        """summarize the kpis of the property"""
        return pd.DataFrame(
            data=[
                round(self.gross_rental_yield * 100, 2),
                round(self.net_rental_yield * 100, 2),
                round(self.multiplication_factor, 2),
                round(self.return_on_equity * 100, 2),
                round(self.ten_year_net_capital_gain(), 2),
                round(self.ten_year_roe() * 100, 2),
            ],
            index=[  # pyright: ignore[reportArgumentType]
                "Gross Rental Yield",
                "Net Rental Yield",
                "Multiplication Factor",
                "Return on Equity",
                "10 Year Net Capital Gain",
                "10 Year RoE",
            ],
        )

    def eval_dict(self) -> dict:
        return {
            "Gross Rental Yield": round(self.gross_rental_yield * 100, 2),
            "Net Rental Yield": round(self.net_rental_yield * 100, 2),
            "Multiplication Factor": round(self.multiplication_factor, 2),
            "Return on Equity": round(self.return_on_equity * 100, 2),
            "10 Year Net Capital Gain": round(self.ten_year_net_capital_gain(), 2),
            "10 Year RoE": round(self.ten_year_roe() * 100, 2),
        }

    def to_dict(self) -> dict:
        return {key: value.__dict__ for key, value in self.__dict__.items()}

    def to_json(self) -> str:
        import json

        return json.dumps(self.to_dict())

    def pickle(self) -> str:
        return pickle.dumps(self, 0).decode("ascii")

    def set_price(self, price: float) -> None:
        self.base_cost.set_price(price)
        self.mortgage.amount = self.base_cost.loan

    def set_modernisation(self, value: float) -> None:
        self.base_cost.set_modernisation(value)

    def set_agent(self, value: float) -> None:
        self.base_cost.set_agent(value)
        self.mortgage.amount = self.base_cost.loan

    def set_agent_rate(self, value: float) -> None:
        self.base_cost.set_agent_rate(value)
        self.mortgage.amount = self.base_cost.loan

    def set_property_buy_tax(self, value: float) -> None:
        self.base_cost.set_property_buy_tax(value)
        self.mortgage.amount = self.base_cost.loan

    def set_property_buy_tax_rate(self, value: float) -> None:
        self.base_cost.set_property_buy_tax_rate(value)
        self.mortgage.amount = self.base_cost.loan

    def set_notary(self, value: float) -> None:
        self.base_cost.set_notary(value)
        self.mortgage.amount = self.base_cost.loan

    def set_notary_rate(self, value: float) -> None:
        self.base_cost.set_notary_rate(value)
        self.mortgage.amount = self.base_cost.loan

    def set_land_registry(self, value: float) -> None:
        self.base_cost.set_land_registry(value)
        self.mortgage.amount = self.base_cost.loan

    def set_land_registry_rate(self, value: float) -> None:
        self.base_cost.set_land_registry_rate(value)
        self.mortgage.amount = self.base_cost.loan

    def set_proprietary_capital(self, value: float) -> None:
        self.base_cost.set_proprietary_capital(value)
        self.mortgage.amount = self.base_cost.loan

    def set_proprietary_capital_rate(self, value: float) -> None:
        self.base_cost.set_proprietary_capital_rate(value)
        self.mortgage.amount = self.base_cost.loan

    def set_loan(self, value: float) -> None:
        self.base_cost.set_loan(value)
        self.mortgage.amount = self.base_cost.loan

    def set_loan_rate(self, value: float) -> None:
        self.base_cost.set_loan_rate(value)
        self.mortgage.amount = self.base_cost.loan

    def set_net_cold_rent_monthly(self, value: float) -> None:
        self.cash_flow.set_net_cold_rent(value)

    def set_net_cold_rent_annually(self, value: float) -> None:
        self.cash_flow.set_net_cold_rent(value / 12)

    def set_operating_income_monthly(self, value: float) -> None:
        self.cash_flow.set_operating_income(value)

    def set_operating_income_annually(self, value: float) -> None:
        self.cash_flow.set_operating_income(value / 12)

    def set_operating_expenses_monthly(self, value: float) -> None:
        self.cash_flow.set_operating_expenses(abs(value))

    def set_operating_expenses_annually(self, value: float) -> None:
        self.cash_flow.set_operating_expenses(abs(value / 12))

    def set_annuity_monthly(self, value: float) -> None:
        self.mortgage.update_annuity(abs(value * 12))

    def set_annuity_annually(self, value: float) -> None:
        self.mortgage.update_annuity(abs(value))

    def set_interest_rate(self, value: float) -> None:
        self.mortgage.update_interest_rate(value)

    def set_repay_time_total(self, value: float) -> None:
        self.mortgage.update_repay_time(value)

    def set_repayment_rate(self, value: float) -> None:
        self.mortgage.update_repayment_rate(value)

    def set_living_space(self, value: float) -> None:
        self.details.living_space = value

    def set_price_per_sqm(self, value: float) -> None:
        self.set_price(value * self.details.living_space)

    def set_rent_per_sqm(self, value: float) -> None:
        self.set_net_cold_rent_monthly(value * self.details.living_space)

    def update(self, card: str, field: str, attribute: str, value: float) -> Self:
        attr_map = {
            ("base_cost", "price", "total"): "set_price",
            ("base_cost", "modernisation", "total"): "set_modernisation",
            ("base_cost", "agent", "total"): "set_agent",
            ("base_cost", "agent", "rate"): "set_agent_rate",
            ("base_cost", "property buy tax", "total"): "set_property_buy_tax",
            ("base_cost", "property buy tax", "rate"): "set_property_buy_tax_rate",
            ("base_cost", "notary", "total"): "set_notary",
            ("base_cost", "notary", "rate"): "set_notary_rate",
            ("base_cost", "land registry", "total"): "set_land_registry",
            ("base_cost", "land registry", "rate"): "set_land_registry_rate",
            ("base_cost", "proprietary capital", "total"): "set_proprietary_capital",
            (
                "base_cost",
                "proprietary capital",
                "rate",
            ): "set_proprietary_capital_rate",
            ("base_cost", "loan", "total"): "set_loan",
            ("base_cost", "loan", "rate"): "set_loan_rate",
            ("cash_flow", "net cold rent", "monthly"): "set_net_cold_rent_monthly",
            ("cash_flow", "net cold rent", "annually"): "set_net_cold_rent_annually",
            (
                "cash_flow",
                "operating income",
                "monthly",
            ): "set_operating_income_monthly",
            (
                "cash_flow",
                "operating income",
                "annually",
            ): "set_operating_income_annually",
            (
                "cash_flow",
                "operating expenses",
                "monthly",
            ): "set_operating_expenses_monthly",
            (
                "cash_flow",
                "operating expenses",
                "annually",
            ): "set_operating_expenses_annually",
            ("cash_flow", "annuity", "monthly"): "set_annuity_monthly",
            ("cash_flow", "annuity", "annually"): "set_annuity_annually",
            ("mortgage", "interest rate", "-"): "set_interest_rate",
            ("mortgage", "annuity", "-"): "set_annuity_annually",
            ("mortgage", "repay time total", "-"): "set_repay_time_total",
            ("mortgage", "initial repayment rate", "-"): "set_repayment_rate",
            ("cost_effectiveness", "living space", "-"): "set_living_space",
            ("cost_effectiveness", "price/sqm", "-"): "set_price_per_sqm",
            ("cost_effectiveness", "net cold rent/sqm", "-"): "set_rent_per_sqm",
        }

        key = (card, field, attribute)
        if key in attr_map:
            getattr(self, attr_map[key])(value)
        else:
            raise ValueError(f"Cannot update {field} {attribute}")
        return self


def depickle(b_immo: str) -> Immo:
    cur_immo = pickle.loads(b_immo.encode("ascii"))
    if not isinstance(cur_immo, Immo):
        raise TypeError("decoding has the wrong instance")
    return cur_immo
