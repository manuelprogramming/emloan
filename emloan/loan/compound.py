from typing import Iterable, Union


import numpy as np
import pandas as pd
import plotly.graph_objects as go

from . import installments


def annualized_interest(end_capital:float, starting_capital:float, period:int) -> float:
    return (end_capital/starting_capital)**(1/period)-1


def compound_interest(starting_capital: float, # starting capital
                      interest_rate: float, 
                      period: int, 
                      installment: Union[float, int, Iterable] = 0,
                      installment_type: str = "fixed",
                      **kwargs) -> tuple[float, float]:
    """calculates the total amount earned given installments starting capital
    returns: total amount with interest and total set capital"""
    cn = starting_capital * (1+interest_rate)**period
    
    if installment == 0:
        return round(cn,2), starting_capital

    installment_array = installments.create_installment(period, installment, installment_type, **kwargs)
    installment_interests = np.array([installment_array[i] * (1+interest_rate)**(period-i) for i in range(period)]).sum()

    
    total_net = cn + installment_interests
    equity = starting_capital + installment_array.sum()
    return round(total_net,2), equity


def compound_interest_detailed(starting_capital: float, # starting capital
                               interest_rate: float, 
                               period: int, 
                               installment: Union[float, int, Iterable] = 0,
                               installment_type: str = "fixed",
                               **kwargs) -> pd.DataFrame:
    
    periods = np.arange(1, period+1,1)
    
    column_names= ["Period","Equity", "Interest", "Total"]
    compound_df = pd.DataFrame(columns=column_names)
    for period_delta in periods:
        total_net,equity = compound_interest(starting_capital = starting_capital,
                                             interest_rate = interest_rate,
                                             period = period_delta,
                                             installment = installment,
                                             installment_type=installment_type,
                                             **kwargs)
        cur_df = pd.DataFrame(columns=column_names)
        cur_df.loc[0] = [period_delta, equity, total_net-equity, total_net]
        compound_df = pd.concat([
            compound_df if not compound_df.empty else None,
            cur_df], axis=0)
    
    compound_df.reset_index(inplace=True, drop=True)
    return compound_df



def compound_interest_plot(compound_df: pd.DataFrame) -> go.Figure:
    import plotly.express as px
    fig = px.bar(compound_df, x='Period', y=['Equity', "Interest"])
    return fig
    