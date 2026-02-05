import numpy as np
import pandas as pd

import plotly.graph_objects as go


def annuity_from_period(loan_amount: int, interest_rate: float, period: int) -> float:
    disount_factor = (1 / (1 + interest_rate)) ** int(period)
    return round(loan_amount * interest_rate / (1 - disount_factor), 2)


def loan_period(loan_amount: int, annuity: float, interest_rate: float) -> float:
    if interest_rate * loan_amount / annuity >= 1:
        raise ValueError(
            "The annuity must be greater than the interest rate times the credit"
        )

    return np.log(1 - (interest_rate * loan_amount / annuity)) / np.log(
        1 / (1 + interest_rate)
    )


def annuity_from_repayment_rate(
    loan_amount: int, interest_rate, repayment_rate: float = 0.01
) -> float:
    return round((loan_amount * repayment_rate) + loan_amount * interest_rate)


def repayment_rate_from_annuity(
    loan_amount: float, interest_rate: float, annuity: float
) -> float:
    return annuity / loan_amount - interest_rate


def rest_dept(
    loan_amount: float,
    interest_rate: float,
    period: int,
    annuity: float,
    hist: bool = False,
) -> pd.DataFrame:
    if period == 0:
        return loan_amount
    if loan_amount == 0:
        return 0
    if interest_rate < 0:
        raise ValueError("Negative Interest Rate are not possible for this calculation")

    column_names = ["Period", "Credit Pre", "Interest", "Repay", "Credit Post"]
    dept_hist = pd.DataFrame()
    credit_post = loan_amount
    max_period = period

    for period in range(1, max_period + 1):
        credit_pre = credit_post
        interest = credit_pre * interest_rate
        repay = annuity - interest
        credit_post = round(credit_pre - repay, 2)
        cur_df = pd.DataFrame(columns=column_names)
        cur_df.loc[0] = [period, credit_pre, interest, repay, credit_post]
        dept_hist = pd.concat([dept_hist, cur_df], axis=0)
    if hist:
        return dept_hist
    else:
        return dept_hist["Credit Post"].iloc[-1]


def plot_credit_repay_hist(res_df: pd.DataFrame) -> go.Figure:

    from plotly.subplots import make_subplots

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=list(res_df.Period),
            y=list(res_df.Interest),
            name="Interest",
            hovertemplate="Paid Interest: %{y:.0f}",
        )
    )

    fig.add_trace(
        go.Bar(
            x=list(res_df.Period),
            y=list(res_df.Repay),
            name="Repay",
            hovertemplate="Repayed Credit: %{y:.0f}",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=list(res_df.Period),
            y=list(res_df["Credit Post"]),
            name="Post Period Credit",
            hovertemplate="Post Period Credit: %{y:.0f}",
        ),
        secondary_y=True,
    )

    fig.update_layout(barmode="stack", hovermode="x", autosize=False)

    fig.update_yaxes(title_text="Annuity", secondary_y=False)
    fig.update_yaxes(title_text="Rest Credit Amount", secondary_y=True)
    fig.update_xaxes(title_text="Period")

    return fig
