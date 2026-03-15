from market.gbm import GBMMarket
from strats.momentum import MomentumStrategy
from execution.portfolio import Portfolio
from core.backtester import Backtester
from analytics.montecarlo import run_monte_carlo
from analytics.plot import plot_equity
from analytics.metrics import total_return, max_drawdown
import time

DAYS_IN_YEAR = 252
YEARS = 2

if __name__ == "__main__":

    # Instead of inserting constructed objects, we call a mini function each time to refresh
    # Therefore no more monte carlo bugs
    backtester = Backtester(
            market_factory=lambda: GBMMarket(0.07, 0.15, 100, dt=1/252),
            strategy_factory=lambda: MomentumStrategy(lookback=20, threshold=0),
            portfolio_factory=lambda strategy, market:
                Portfolio(200, strategy, market, 0.01, 0.01)
        )
    result = backtester.run(1, True)
    equity = result["equity"]

    print(f"Total return: {total_return(equity):.3f}")
    print(f"Max drawdown: {max_drawdown(equity):.3f}")

    start_time = time.perf_counter()
    total_results = run_monte_carlo(backtester, 500, 1)
    end_time = time.perf_counter()

    print("---MONTE CARLO SIM AVGS---")
    print(f"Sharpe: {total_results['sharpe']:.3f}")
    print(f"Max Drawdown: {total_results['max_dd']:.3f}")
    print(f"Return: {total_results['return']:.3f}")
    print(f"Time Taken: {end_time - start_time:.3f}s")

    

    

    
    
    
