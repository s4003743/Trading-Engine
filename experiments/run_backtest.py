from core.backtester import Backtester
from collections import defaultdict


def run_backtest(backtester : Backtester, n : int, num_years : int) -> dict:
    """
    Takes in `Backtester` object and runs simulation `n` to produce 
    average results/statistics on the success of the strategy on 
    the applied market.
    """
    raise NotImplementedError
