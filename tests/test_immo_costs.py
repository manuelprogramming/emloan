import pytest

from emloan import immo


@pytest.fixture
def default_basecost() -> immo.BaseCost:
    return immo.BaseCost(price=100_000)


def test_default_values(default_basecost: immo.BaseCost):
    assert default_basecost.price == 100000
    assert default_basecost.modernisation == 0
    assert default_basecost.property_buy_tax_rate == 0.055
    assert default_basecost.agent_rate == 0.0357
    assert default_basecost.notary_rate == 0.015
    assert default_basecost.land_registry_rate == 0.005
    assert default_basecost.proprietary_capital_rate == 0.2
    assert default_basecost.loan_rate == 0.8


def test_proprietary_capital_and_loan_rate(default_basecost: immo.BaseCost):
    assert default_basecost.proprietary_capital_rate + default_basecost.loan_rate == 1


@pytest.mark.parametrize("proprietary_capital_rate", [-0.4, 0, 0.1, 0.5, 1, 1.3, 100])
def test_different_proprietary_capital_rates(
    default_basecost: immo.BaseCost, proprietary_capital_rate: float
):
    default_basecost.set_proprietary_capital_rate(proprietary_capital_rate)
    if proprietary_capital_rate > 1:
        assert default_basecost.proprietary_capital_rate == 1
    elif proprietary_capital_rate < 0:
        assert default_basecost.proprietary_capital_rate == 0
    else:
        assert default_basecost.proprietary_capital_rate == proprietary_capital_rate

    assert default_basecost.proprietary_capital_rate + default_basecost.loan_rate == 1


@pytest.mark.parametrize("loan_rate", [-0.4, 0, 0.1, 0.5, 1, 1.3, 100])
def test_different_loan_rates(default_basecost: immo.BaseCost, loan_rate: float):
    default_basecost.set_loan_rate(loan_rate)
    if loan_rate > 1:
        assert default_basecost.loan_rate == 1
    elif loan_rate < 0:
        assert default_basecost.loan_rate == 0
    else:
        assert default_basecost.loan_rate == loan_rate

    assert default_basecost.proprietary_capital_rate + default_basecost.loan_rate == 1


def test_calculations_from_rates(default_basecost: immo.BaseCost):
    assert (
        default_basecost.notary == default_basecost.notary_rate * default_basecost.price
    )
    assert (
        default_basecost.property_buy_tax
        == default_basecost.property_buy_tax_rate * default_basecost.price
    )
    assert (
        default_basecost.land_registry
        == default_basecost.land_registry_rate * default_basecost.price
    )
    assert default_basecost.agent == round(
        default_basecost.agent_rate * default_basecost.price, 2
    )


@pytest.mark.parametrize("notary_rate", [-0.4, 0, 0.2, 0.5, 1, 1.3])
def test_set_notary_rate(default_basecost: immo.BaseCost, notary_rate: float):
    default_basecost.set_notary_rate(notary_rate)
    if notary_rate < 0:
        assert default_basecost.notary_rate == 0
    else:
        assert default_basecost.notary_rate == notary_rate


@pytest.mark.parametrize("property_buy_tax_rate", [-0.4, 0, 0.2, 0.5, 1, 1.3])
def test_set_property_buy_tax_rate(
    default_basecost: immo.BaseCost, property_buy_tax_rate: float
):
    default_basecost.set_property_buy_tax_rate(property_buy_tax_rate)
    if property_buy_tax_rate < 0:
        assert default_basecost.property_buy_tax_rate == 0
    else:
        assert default_basecost.property_buy_tax_rate == property_buy_tax_rate


@pytest.mark.parametrize("land_registry_rate", [-0.4, 0, 0.2, 0.5, 1, 1.3])
def test_set_land_registry_rate(
    default_basecost: immo.BaseCost, land_registry_rate: float
):
    default_basecost.set_land_registry_rate(land_registry_rate)
    if land_registry_rate < 0:
        assert default_basecost.land_registry_rate == 0
    else:
        assert default_basecost.land_registry_rate == land_registry_rate


@pytest.mark.parametrize("agent_rate", [-0.4, 0, 0.2, 0.5, 1, 1.3])
def test_set_agent_rate(default_basecost: immo.BaseCost, agent_rate: float):
    default_basecost.set_agent_rate(agent_rate)
    if agent_rate < 0:
        assert default_basecost.agent_rate == 0
    else:
        assert default_basecost.agent_rate == agent_rate


@pytest.mark.parametrize("notary", [-500, 0, 5_000, 10_000])
def test_set_notary(default_basecost: immo.BaseCost, notary: float):
    default_basecost.set_notary(notary)
    if notary < 0:
        assert default_basecost.notary == 0
    else:
        assert default_basecost.notary == notary
        assert default_basecost.notary_rate == notary / default_basecost.price


@pytest.mark.parametrize("property_buy_tax", [-500, 0, 5_000, 10_000])
def test_set_property_buy_tax(default_basecost: immo.BaseCost, property_buy_tax: float):
    default_basecost.set_property_buy_tax(property_buy_tax)
    if property_buy_tax < 0:
        assert default_basecost.property_buy_tax == 0
    else:
        assert default_basecost.property_buy_tax == property_buy_tax
        assert (
            default_basecost.property_buy_tax_rate
            == property_buy_tax / default_basecost.price
        )


@pytest.mark.parametrize("land_registry", [-500, 0, 5_000, 10_000])
def test_set_land_registry(default_basecost: immo.BaseCost, land_registry: float):
    default_basecost.set_land_registry(land_registry)
    if land_registry < 0:
        assert default_basecost.land_registry == 0
    else:
        assert default_basecost.land_registry == land_registry
        assert (
            default_basecost.land_registry_rate
            == land_registry / default_basecost.price
        )


@pytest.mark.parametrize("loan_amount", [-500, 0, 5_000, 10_000, 200_000])
def test_set_loan(default_basecost: immo.BaseCost, loan_amount: float):
    default_basecost.set_loan(loan_amount)
    if loan_amount < 0:
        assert default_basecost.loan == 0
    elif loan_amount > default_basecost.total:
        assert default_basecost.loan == default_basecost.total
    else:
        assert default_basecost.loan == loan_amount
        assert default_basecost.loan_rate == loan_amount / default_basecost.total


@pytest.mark.parametrize("proprietary_capital", [-500, 0, 5_000, 10_000, 200_000])
def test_set_proprietary_capital(
    default_basecost: immo.BaseCost, proprietary_capital: float
):
    default_basecost.set_proprietary_capital(proprietary_capital)
    if proprietary_capital < 0:
        assert default_basecost.proprietary_capital == 0
    elif proprietary_capital > default_basecost.total:
        assert default_basecost.proprietary_capital == default_basecost.total
    else:
        assert default_basecost.proprietary_capital == proprietary_capital
        assert (
            default_basecost.proprietary_capital_rate
            == proprietary_capital / default_basecost.total
        )

@pytest.mark.parametrize("modernisation", [-500, 0, 5_000, 1_000_000])
def test_set_modernisation(default_basecost: immo.BaseCost, modernisation: float):
    default_basecost.set_modernisation(modernisation)

    if modernisation < 0:
        assert default_basecost.modernisation == 0
    else:
        assert default_basecost.modernisation == modernisation
    
def test_total(default_basecost: immo.BaseCost):
    default_basecost.set_modernisation(10_000)
    assert default_basecost.total == default_basecost.price + default_basecost.modernisation + default_basecost.extras