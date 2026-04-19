from pathlib import Path
from collections import defaultdict
from typing import Literal

import numpy as np
import pandas as pd
from scipy import stats

VALID_DISTRIBUTIONS = ["norm", "weibull_min", "gennorm"]


from enum import Enum

class Timing(Enum):
    BEGIN = "begin"
    END = "end"


def _get_rv(data: pd.DataFrame, dist_name: str = "norm") -> stats.rv_continuous:
    if not dist_name in VALID_DISTRIBUTIONS:
        raise ValueError(
            f"Ditribution {dist_name} is not available. Choose from {VALID_DISTRIBUTIONS}"
        )

    dist = getattr(stats, dist_name)
    params = dist.fit(data.log_return)
    return dist(*params)


def fit_data(data: pd.DataFrame, dist_name: str = "norm") -> tuple[np.ndarray, np.ndarray]:
    step = 0.01
    samples = 1000
    # data = get_monthly_return_data(dataset)

    x_sim = np.linspace(
        data.monthly_return_pct.min() - step,
        data.monthly_return_pct.max() + step,
        samples,
    )
    rv = _get_rv(data, dist_name)
    return x_sim, rv.pdf(x_sim)


def calculate_return_mc(
    data: pd.DataFrame,
    periods: int,
    installment: float,
    dist_name: str,
    n_sims: int,
    initial_investment: float = 0.0,
    annual_fee: float = 0.0,
    timing: Timing = Timing.BEGIN,
):
    # --- prepare data ---
    data = data.copy()

    dist = _get_rv(data, dist_name)

    # --- simulate log returns ---
    log_returns = dist.rvs((n_sims, periods))

    # --- fees in log space ---
    log_fee = np.log(1 - annual_fee) / 12
    log_returns_net = log_returns + log_fee

    # --- growth ---
    log_growth = np.cumsum(log_returns_net, axis=1)
    growth = np.exp(log_growth)

    # --- initial investment ---
    initial_value = initial_investment * growth[:, -1]

    # --- installments ---
    if timing == Timing.BEGIN:
        installment_value = (installment * growth).sum(axis=1)
    else:
        installment_value = (installment * growth[:, 1:]).sum(axis=1)

    return initial_value + installment_value



if __name__ == "__main__":
    #data = get_monthly_return_data()
    # print(data.to_dict(orient="list"))
    periods = 20 * 12  # 20 years
    installment = 250
    n_runs = 10000
