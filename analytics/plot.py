import matplotlib.pyplot as plt
from strats.base_strat import Move

def plot_equity(equity_history, market_prices=None, trade_history=None):
    fig, ax1 = plt.subplots(figsize=(10,5))
    ax2 = None  # initialize

    # Plot portfolio equity
    ax1.plot(equity_history, label='Equity', color='blue')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Equity', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Plot market price on secondary y-axis if provided
    if market_prices is not None:
        ax2 = ax1.twinx()
        ax2.plot(market_prices, label='Market Price', color='brown', alpha=0.6)
        ax2.set_ylabel('Market Price', color='brown')
        ax2.tick_params(axis='y', labelcolor='brown')

    # Overlay trades
    if trade_history is not None and not trade_history.empty:
        buy_trades = trade_history[trade_history['signal'] == Move.BUY]
        sell_trades = trade_history[trade_history['signal'] == Move.SELL]
        ax1.scatter(buy_trades['time'], buy_trades['price'], color='green', marker='^', s=100, label='BUY')
        ax1.scatter(sell_trades['time'], sell_trades['price'], color='red', marker='v', s=100, label='SELL')

    # Legend (combined from both axes)
    lines, labels = ax1.get_legend_handles_labels()
    if ax2 is not None:
        lines2, labels2 = ax2.get_legend_handles_labels()
        lines += lines2
        labels += labels2
    ax1.legend(lines, labels, loc='best')

    plt.title('Portfolio Equity and Market Price with Trades')
    plt.grid(True)
    plt.show()