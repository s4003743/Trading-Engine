from .metrics import total_return, max_drawdown, sharpe_ratio
from core.backtester import Backtester

def run_monte_carlo(backtester : Backtester, n, years) -> dict:
    """
    Formalised version of `run_backtest`. Runs numerous 
    simulations dictated by `n` and returns the average 
    result.
    """

    results = []

    for _ in range(n):
        result = backtester.run(years)
        equity = result["equity"]

        stats = {
            "return": total_return(equity),
            "max_dd": max_drawdown(equity),
            "sharpe": sharpe_ratio(equity),
        }
        results.append(stats)

    avg = {
        k: sum(r[k] for r in results) / n
        for k in results[0]
    }

    return avg