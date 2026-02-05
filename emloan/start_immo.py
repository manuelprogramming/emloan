from pathlib import Path
import json

from . import calculators
from . import immo


def start_immo() -> immo.Immo:
    repay_rate = 0.08
    annuity = 1400 * 12
    interest_rate = 0.0325
    period = 25

    data_dir = Path("data")
    cur_file = data_dir / "house.json"

    with open(cur_file) as json_file:
        prop_data = json.load(json_file)

    return calculators.calc_property_by_period(prop_data, interest_rate, period)
