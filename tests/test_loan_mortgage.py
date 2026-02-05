import pytest

from emloan import loan


@pytest.fixture
def default_mortgage() -> loan.Mortgage:
    """Fixture that returns a Mortgage instance with default optional values."""
    amount = 100000.0
    interest_rate = 0.025
    period = 10

    annuity = loan.annuity_from_period(
        loan_amount=amount, interest_rate=interest_rate, period=period
    )

    repayment_rate = loan.repayment_rate_from_annuity(
        loan_amount=amount, interest_rate=interest_rate, annuity=annuity
    )

    return loan.Mortgage(
        amount=amount,
        _annuity=annuity,
        interest_rate=interest_rate,
        _period=period,
        _repayment_rate=repayment_rate,
    )


def test_default_values(default_mortgage: loan.Mortgage):
    assert default_mortgage.amount == 100000
    assert default_mortgage.annuity == loan.annuity_from_period(
        loan_amount=default_mortgage.amount,
        interest_rate=default_mortgage.interest_rate,
        period=default_mortgage.period,
    )
    assert default_mortgage.interest_rate == 0.025
    assert default_mortgage.period == 10
    assert default_mortgage.repayment_rate == loan.repayment_rate_from_annuity(
        loan_amount=default_mortgage.amount,
        interest_rate=default_mortgage.interest_rate,
        annuity=default_mortgage.annuity,
    )


def test_custom_values():
    m = loan.Mortgage(
        amount=200000, _annuity=5000, interest_rate=3.0, _period=20, _repayment_rate=2.0
    )
    assert m.amount == 200000
    assert m.annuity == 5000
    assert m.interest_rate == 3.0
    assert m.period == 20
    assert m.repayment_rate == 2.0


def test_missing_required_fields():
    with pytest.raises(TypeError):
        loan.Mortgage()  # Missing required fields


def test_type_acceptance(default_mortgage: loan.Mortgage):
    # dataclass accepts wrong types unless explicitly validated
    assert isinstance(default_mortgage.amount, float)
    assert isinstance(default_mortgage.annuity, float)
    assert isinstance(default_mortgage.interest_rate, float)


@pytest.mark.parametrize("annuity", [1000, 5000, 100000])
def test_update_annuity(default_mortgage: loan.Mortgage, annuity: float):
    init_repayment_rate = default_mortgage.repayment_rate
    default_mortgage.update_annuity(annuity)
    assert default_mortgage.annuity == annuity
    # make sure rapyment_rate is also updated
    assert init_repayment_rate != default_mortgage.repayment_rate


@pytest.mark.parametrize("repayment_rate", [0.1, 0.2, 0.5])
def test_update_repayment_rate(default_mortgage: loan.Mortgage, repayment_rate: float):
    init_annuity = default_mortgage.annuity
    default_mortgage.update_repayment_rate(repayment_rate)
    assert default_mortgage.repayment_rate == repayment_rate
    # make sure annuity is also updated
    assert default_mortgage.annuity != init_annuity


@pytest.mark.parametrize("interest_rate", [0.03, 0.05, 0.07])
def test_update_interest_rate(default_mortgage: loan.Mortgage, interest_rate: float):
    default_mortgage.update_interest_rate(interest_rate)

    assert default_mortgage.interest_rate == interest_rate


@pytest.mark.parametrize("repay_time", [2, 15, 32.3, 100])
def test_update_repay_time(default_mortgage: loan.Mortgage, repay_time: int):
    init_annuity = default_mortgage.annuity
    init_repayment_rate = default_mortgage.repayment_rate

    default_mortgage.update_repay_time(repay_time)

    assert default_mortgage.repay_time_total == round(repay_time)
    assert default_mortgage.annuity != init_annuity
    assert default_mortgage.repayment_rate != init_repayment_rate


def test_summary_dict(default_mortgage: loan.Mortgage):
    expected_keys = {
        "Interest Rate",
        "Initial Repayment Rate",
        "Annuity",
        "Repay Time Total",
    }
    summary = default_mortgage.summary_dict()
    actual_keys = set(summary.keys())

    assert (
        actual_keys == expected_keys
    ), f"Expected keys: {expected_keys}, but got: {actual_keys}"
