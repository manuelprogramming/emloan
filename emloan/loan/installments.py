import numpy as np
from typing import Union, Iterable
from dataclasses import dataclass

from .errors import WrongInstallmentRateError, WrongInstallmentTypeError, CustomInstallmentWrongLengthError

def fixed_installment(period: Union[int, float], rate: float) -> np.ndarray:
    if not isinstance(rate, (int, float)):
        raise WrongInstallmentRateError("When specifying fixed installment the rate must be of type int or float")
    return np.full(period, rate)

def dynamic_installment(period: int, rate: float, factor: float) -> np.ndarray:
    return np.array([rate*(1+factor)**i for i in range(period)])

def custom_installment(period: int, rate: Iterable[float]) -> np.ndarray:
    try:
        _ = iter(rate)
    except TypeError as te:
        raise TypeError(rate, 'is not iterable')
    
    rate = np.array(rate)
    if not period == len(rate):
        raise CustomInstallmentWrongLengthError("When specifying Custom Installment the period must have the same length as the rate array")
    return rate

def create_installment(period: int,
                       rate: Union[float, Iterable],
                       installment_type: str = "fixed",
                       **kwargs) -> np.array:
    match installment_type:
        case "fixed": 
            return fixed_installment(period = period, rate = rate)
        case "dynamic": 
            return dynamic_installment(period = period, rate = rate, **kwargs)
        case "custom":
            return custom_installment(period, rate)
        case _ : 
            raise WrongInstallmentTypeError("The installment type you specified does not exist")  





        
    