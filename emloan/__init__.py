from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("emloan")
except PackageNotFoundError:
    __version__ = "0.0.0"


from . import calculators
from . import loan
from . import immo
from .start_immo import start_immo
from . import etf_montecarlo
