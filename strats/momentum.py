from .base_strat import Strategy, Move
import numpy as np
from market.gbm import GBMMarket

class MomentumStrategy(Strategy):
    def __init__(self, lookback, threshold) -> None:
        self.lookback = lookback
        self.threshold = threshold

    def generate_signal(self, market) -> Move:
        """
        Returns move recommendation based on market state.

        Momentum works by simply checking whether the latest 
        price is above the average for a given window. Then 
        it moves according to the potential upward or downward 
        trajectory of the market.
        """
        history = market.get_price_history(self.lookback)
        if len(history) < self.lookback:
            return Move.HOLD
        elif abs(history[-1] - np.mean(history)) < self.threshold:
            return Move.HOLD
        elif history[-1] > np.mean(history):
            return Move.BUY
        else:
            return Move.SELL




if __name__ == "__main__":
    market = GBMMarket(0.07, 0.15, 100, dt=1/252)
    strategy = MomentumStrategy(lookback=20, threshold=2)

    for _ in range(50):
        market.step()
        signal = strategy.generate_signal(market)
        print(f"Time {market.get_time()}, Price {market.get_price():.2f}, Signal {signal.name}")