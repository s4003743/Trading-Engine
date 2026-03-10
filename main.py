from market.gbm import GBMMarket
from strats.momentum import MomentumStrategy
from execution.portfolio import Portfolio
from analytics.metrics import trade_stats, total_return, max_drawdown
from analytics.plot import plot_equity
import pandas as pd
from core.backtester import Backtester

DAYS_IN_YEAR = 252
YEARS = 2

if __name__ == "__main__":
    market = GBMMarket(0.03, 0.15, 10, dt=1/DAYS_IN_YEAR)
    strategy = MomentumStrategy(lookback=20, threshold=0.00)
    portfolio = Portfolio(200, strategy, market, 0.01, 0.01)
    backtester = Backtester(market, strategy, portfolio)
    backtester.run(3)
    
