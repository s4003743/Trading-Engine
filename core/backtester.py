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

    def __init__(self, market: GBMMarket, strategy: Strategy, portfolio: Portfolio) -> None:
        self.market = market
        self.strategy = strategy
        self.portfolio = portfolio

    def run(self, num_years) -> None:
        """
        Run market and strategy and track portfolio status. 
        Provides stats on the success of the strategy as well 
        as a plot.
        """

        start_portfolio = f"Cash: ${self.portfolio.cash:.2f} | Position: {self.portfolio.position}"

        for _ in range(DAYS_IN_YEAR * num_years):
            self.market.step()
            self.portfolio.update_portfolio()
        
        trade_history = pd.DataFrame(self.portfolio.get_trade_history(), columns=['time','signal','price','position'])
        equity_history = self.portfolio.get_equity_history()
        trade_info = trade_stats(pd.DataFrame(trade_history))

        print("\n---STARTING STATE---\n")
        print(start_portfolio)
        print("\n---FINAL STATE---\n")
        print(self.portfolio)
        print("\n---FINAL EQUITY---\n")
        print(f"Equity: ${self.portfolio.get_equity(self.market.get_price()):.2f}")
        print("\n---FINAL STATS---\n")

        if trade_info is not None:
            print(f"Number of trades: {trade_info['n_trades']}")
            print(f"Win rate: {trade_info['win_rate']:.2f}")
            print(f"Avg return: {trade_info['avg_return']:.2f}")
        print(f"Max drawdown: {max_drawdown(equity_history):.2f}")
        print(f"Sharpe ratio: {sharpe_ratio(equity_history):.2f}")
        print(f"Total return: {total_return(equity_history):.2f}\n")

        plot_equity(self.portfolio.get_equity_history(), self.portfolio.market.get_price_history(), trade_history)