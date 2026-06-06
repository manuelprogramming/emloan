from dataclasses import dataclass
import pandas as pd
import plotly.graph_objects as go

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


def cap_dev_plot(scenarios_df: pd.DataFrame, proprietary_capital: float = None):
    color_map = {"good": "#16a34a", "medium": "#f59e0b", "bad": "#dc2626"}
    fig = go.Figure()

    proprietary_capital = proprietary_capital if proprietary_capital > 0 else 1

    for scenario in color_map.keys():
        scenarios_df[scenario + "gain"] = scenarios_df[scenario] / proprietary_capital

        fig.add_scatter(
            x=scenarios_df["Period"],
            y=scenarios_df[scenario],
            marker_color=color_map[scenario],
            name=scenario,
            customdata=list(
                scenarios_df[
                    [scenario + "gain", scenario + " Annualized Return"]
                ].itertuples(index=False, name=None)
            ),
            hovertemplate="<b>Scenario:</b> %{fullData.name}<br>"
            + "<b>Year:</b> %{x}<br>"
            + "<b>Capital:</b> €%{y:,.2f}<br>"
            + "<b>Gain:</b> %{customdata[0]:,.2%}<br>"
            + "<b>Annualized Return:</b> %{customdata[1]:,.2%}"
            + "<extra></extra>",
        )

    fig.add_trace(
        go.Scatter(
            x=[scenarios_df["Period"].min(), scenarios_df["Period"].max()],
            y=[proprietary_capital, proprietary_capital],
            mode="lines",
            line=dict(
                color="#64748b",
                dash="dash",
                width=2,
            ),
            name="Proprietary Capital",
            hoverinfo="skip",
        )
    )

    return fig.update_layout(
        autosize=True,
        height=340,
        width=450,
        dragmode=False,
        showlegend=True,
        xaxis=dict(
            title=dict(
                text="Years",
                standoff=5,
            ),
            showgrid=False,
        ),
        yaxis=dict(
            title=dict(
                text="Amount [€]",
            ),
            showgrid=False,
        ),
        legend=dict(
            orientation="h",
            y=-0.2,
            x=0.5,
            xanchor="center",
            yanchor="top",
            font=dict(size=8),
        ),
        plot_bgcolor="#f0f4f8",
        margin=dict(
            l=50,
            r=50,
            t=20,
            b=60,
        ),
    )
