from dataclasses import dataclass, field
from typing import Literal
import logging

import pandas as pd
import numpy as np

from . import property_buy_tax

log = logging.getLogger(__name__)


@dataclass
class BaseCost:
    price: float
    modernisation: float = 0
    property_buy_tax_rate: float = field(default_factory=property_buy_tax.median)
    agent_rate: float = 0.0357

    notary_rate: float = 0.015
    land_registry_rate: float = 0.005

    proprietary_capital_rate: float = 0.2
    loan_rate: float = 0.8

    @property
    def notary(self) -> float:
        return round(self.price * self.notary_rate, 2)

    @property
    def property_buy_tax(self) -> float:
        return round(self.price * self.property_buy_tax_rate, 2)

    @property
    def land_registry(self) -> float:
        return round(self.price * self.land_registry_rate, 2)

    @property
    def agent(self) -> float:
        return round(self.price * self.agent_rate, 2)

    @property
    def extras_rate(self) -> float:
        return (
            self.notary_rate
            + self.property_buy_tax_rate
            + self.land_registry_rate
            + self.agent_rate
        )

    @property
    def extras(self) -> float:
        return round(self.price * self.extras_rate, 2)

    @property
    def total(self) -> float:
        return round(self.price + self.modernisation + self.extras, 2)

    @property
    def proprietary_capital(self) -> float:
        return round(self.total * self.proprietary_capital_rate, 2)

    @property
    def loan(self) -> float:
        return round(self.total * self.loan_rate, 2)

    def set_price(self, price: float) -> None:
        self.price = price

    def set_modernisation(self, amount: float) -> None:
        if amount < 0:
            amount = 0
        self.modernisation = amount

    def set_property_buy_tax(self, amount: float) -> None:
        if amount < 0:
            amount = 0
            log.info("property buy tax cannot be negative and was set to 0")
        self.property_buy_tax_rate = amount / self.price

    def set_property_buy_tax_rate(self, rate: float) -> None:
        if rate < 0:
            rate = 0
        self.property_buy_tax_rate = rate

    def set_agent(self, amount: float) -> None:
        if amount < 0:
            amount = 0
            log.info("agent amount cannot be negative and was set to 0")
        self.agent_rate = amount / self.price

    def set_agent_rate(self, rate: float) -> None:
        if rate < 0:
            rate = 0
            log.info("agent rate cannot be negative and was set to 0")
        self.agent_rate = rate

    def set_notary(self, amount: float) -> None:
        if amount < 0:
            amount = 0
            log.info("notary amount cannot be negative and was set to 0")
        self.notary_rate = amount / self.price

    def set_notary_rate(self, rate: float) -> None:
        if rate < 0:
            rate = 0
            log.info("notary rate cannot be negative and was set to 0")
        self.notary_rate = rate

    def set_land_registry(self, amount: float) -> None:
        if amount < 0:
            amount = 0
            log.info("land registry amount cannot be negative and was set to 0")
        self.land_registry_rate = amount / self.price

    def set_land_registry_rate(self, rate: float) -> None:
        if rate < 0:
            rate = 0
            log.info("land registry rate cannot be negative and was set to 0")
        self.land_registry_rate = rate

    def set_loan(self, amount: float) -> None:
        if amount < 0:
            amount = 0
            log.info("loan cannot be negative and was set to 0")
        if amount > self.total:
            log.info(
                "loan cannot be greater than total amount of price and was set to total"
            )
            amount = self.total

        self.loan_rate = amount / self.total
        self.proprietary_capital_rate = 1 - self.loan_rate

    def set_loan_rate(self, rate: float) -> None:
        if rate > 1:
            log.info("loan rate cannot be greater than 1 and was set to 1")
            rate = 1
        if rate < 0:
            log.info("loan rate cannot be less than 0 and was set to 0")
            rate = 0
        self.loan_rate = rate
        self.proprietary_capital_rate = 1 - rate

    def set_proprietary_capital(self, amount: float) -> None:
        if amount < 0:
            amount = 0
            log.info("proprietary capital cannot be negative and was set to 0")
        if amount > self.total:
            log.info(
                "proprietary capital cannot be greater than loan ammount and was set to loan ammount"
            )
            amount = self.total

        self.proprietary_capital_rate = amount / self.total
        self.loan_rate = 1 - self.proprietary_capital_rate

    def set_proprietary_capital_rate(self, rate: float) -> None:
        if rate > 1:
            log.info(
                "proprietary capital rate cannot be greater than 1 and was set to 1"
            )
            rate = 1
        elif rate < 0:
            log.info("proprietary capital rate cannot be less than 0 and was set to 0")
            rate = 0

        self.proprietary_capital_rate = rate
        self.loan_rate = 1 - rate

    def summary(self):
        return pd.DataFrame(
            data={
                "Total": [
                    self.price,
                    self.modernisation,
                    self.extras,
                    self.land_registry,
                    self.notary,
                    self.property_buy_tax,
                    self.agent,
                    self.total,
                    self.proprietary_capital,
                    self.loan,
                ],
                "Rate": [
                    None,
                    None,
                    self.extras_rate,
                    self.land_registry_rate,
                    self.notary_rate,
                    self.property_buy_tax_rate,
                    self.agent_rate,
                    None,
                    self.proprietary_capital_rate,
                    self.loan_rate,
                ],
            },
            index=[
                "Price",
                "Modernisation",
                "Extra Cost",
                "Land Registry",
                "Notary",
                "Property Buy Tax",
                "Agent",
                "Total",
                "Proprietary Capital",
                "Loan",
            ],
        )
