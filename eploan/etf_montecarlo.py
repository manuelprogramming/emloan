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
    params = dist.fit(data.monthly_return_pct)
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
    annual_fee: float = 0.0,
    timing: Timing = Timing.BEGIN,  # "begin" or "end"
):  

    # data = get_monthly_return_data(dataset)
    dist = _get_rv(data, dist_name)
    monthly_changes = dist.rvs((n_sims, periods))

    r = 1 + monthly_changes
    monthly_fee = 1 - (1 - annual_fee) ** (1 / 12)
    r_net = r * (1 - monthly_fee)

    log_growth = np.cumsum(np.log(r_net[:, ::-1]), axis=1)
    growth = np.exp(log_growth)

    if timing == Timing.END:
        growth = growth[:, :-1]   # remove one month of compounding

    return installment * growth.sum(axis=1)



if __name__ == "__main__":
    #data = get_monthly_return_data()
    # print(data.to_dict(orient="list"))
    periods = 20 * 12  # 20 years
    installment = 250
    n_runs = 10000
