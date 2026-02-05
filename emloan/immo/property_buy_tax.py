import numpy as np


BW: float = 0.05  # Baden-Württemberg
BY: float = 0.035  # Bayern
BE: float = 0.06  # Berlin
BB: float = 0.065  # Brandenburg
HB: float = 0.05  # Bremen
HH: float = 0.055  # Hamburg
HE: float = 0.06  # Hessen
MV: float = 0.06  # Mecklenburg-Vorpommern
NI: float = 0.05  # Niedersaschsen
NW: float = 0.065  # Nordrhein-Westfalen
RP: float = 0.05  # Rheinland-Pfalz
SL: float = 0.065  # Saarland
SN: float = 0.055  # Sachsen
ST: float = 0.05  # Sachsen-Anhalt
SH: float = 0.065  # Schleswig-Holstein
TH: float = 0.05  # Thüringen


summary: dict[str, float] = {
    "Baden-Württemberg": BW,
    "Bayern": BY,
    "Berlin": BE,
    "Brandenburg": BB,
    "Bremen": HB,
    "Hamburg": HH,
    "Hessen": HE,
    "Mecklenburg-Vorpommern": MV,
    "Niedersachsen": NI,
    "Nordrhein-Westfalen": NW,
    "Rheinland-Pfalz": RP,
    "Saarland": SL,
    "Sachsen": SN,
    "Sachsen-Anhalt": ST,
    "Schleswig-Holstein": SH,
    "Thüringen": TH,
}


def default() -> float:
    return NI


def average() -> float:
    return np.array(list(summary.values())).mean()


def median() -> float:
    return np.median(np.array(list(summary.values())))
