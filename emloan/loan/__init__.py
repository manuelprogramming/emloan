# This file makes the loan directory a Python package
from .compound import annualized_interest, compound_interest, compound_interest_detailed, compound_interest_plot
from .credit import annuity_from_period, loan_period, annuity_from_repayment_rate, rest_dept, plot_credit_repay_hist, repayment_rate_from_annuity
from .mortgage import Mortgage
from .installments import create_installment, custom_installment, dynamic_installment, fixed_installment
