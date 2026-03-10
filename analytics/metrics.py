import numpy as np
import pandas as pd

def total_return(equity_history):
    """
    Provides total return comparing the inital starting 
    equity with the final equity amount in the portfolio 
    after the trading period ends.
    """
    return equity_history[-1] / equity_history[0] - 1

def max_drawdown(equity_history) -> float:
    """
    Calculate the maximum drawdown of an equity curve.
    equity_history: list or pd.Series of equity values over time
    Returns max drawdown as a float (0.0 - 1.0)
    """
    peak = equity_history[0]
    eq = np.array(equity_history, dtype=float)
    peak = eq[0]
    max_dd = 0.0

    for x in eq:
        if x > peak:
            peak = x
        dd = (peak - x) / peak
        if dd > max_dd:
            max_dd = dd

    return max_dd

def sharpe_ratio(equity_history):
    daily_returns = np.diff(equity_history) / equity_history[:-1]
    return np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(252)

def trade_stats(trade_history: pd.DataFrame):
    trades = trade_history.copy()
    if trades.empty:
        print("No trades executed.")
        return {'n_trades': 0, 'win_rate': 0.0, 'avg_return': 0.0}

    trades['return'] = trades['position'].diff().fillna(0) * trades['price']
    n_trades = len(trades)
    win_rate = (trades['return'] > 0).sum() / max(n_trades, 1)
    avg_return = trades['return'].mean()
    return {'n_trades': n_trades, 'win_rate': win_rate, 'avg_return': avg_return}