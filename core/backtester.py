from strats.base_strat import Strategy
from market.gbm import GBMMarket
from strats.momentum import MomentumStrategy
from execution.portfolio import Portfolio
from analytics.metrics import trade_stats, total_return, max_drawdown, sharpe_ratio
from analytics.plot import plot_equity
import pandas as pd
from rich.pretty import pprint


DAYS_IN_YEAR = 252

class Backtester():

    def __init__(self, market_factory, strategy_factory, portfolio_factory) -> None:
        self.market_factory = market_factory
        self.strategy_factory = strategy_factory
        self.portfolio_factory = portfolio_factory

    def run(self, num_years, plot=False) -> dict:
        """
        Run market and strategy and track portfolio status. 
        Provides stats on the success of the strategy as well 
        as a plot.
        """
        market = self.market_factory()
        strategy = self.strategy_factory()
        portfolio = self.portfolio_factory(strategy, market)
        result = {}

        for _ in range(DAYS_IN_YEAR * num_years):
            market.step()
            portfolio.update_portfolio()
        
        trade_history = pd.DataFrame(portfolio.get_trade_history(), columns=['time','signal','price','position'])
        equity_history = portfolio.get_equity_history()

        result = {
            "equity" : equity_history,
            "trades" : trade_history,
        }

        if plot:
            plot_equity(equity_history, portfolio.market.get_price_history(), trade_history)

        return result