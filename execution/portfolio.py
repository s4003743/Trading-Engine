from market.gbm import GBMMarket
from strats.base_strat import Move, Strategy
from strats.momentum import MomentumStrategy
import pandas as pd

class Portfolio():
    def __init__(self, start_cash, strategy : Strategy, market : GBMMarket, commission, margin) -> None:
        self.cash = start_cash
        self.strategy = strategy
        self.market = market       
        self.position = 0
        self.equity_history = [start_cash]
        self.trade_history = []
        self.commission = commission
        self.margin = margin
    
    def __str__(self) -> str:
        return f"Cash: ${self.cash:.2f} | Position: {self.position}"
    
    def update_portfolio(self) -> None:
        """
        Every step the market makes, the portfolio must update accordingly. 
        Simply updates current cash and appends to equity and trade history.
        """

        price = self.market.get_price()
        signal = self.strategy.generate_signal(self.market)
        
        old_position = self.position
        self.update_position(signal, price)

        equity = self.get_equity(price)
        required_margin = abs(self.position * price) * self.margin

        if equity < required_margin:
            self.close_position(price)
            print(f"Margin call at {market.get_time()}.")

        self.equity_history.append(equity)

        # Only log trades, not HOLDS and account for commision is trade was made
        if old_position != self.position:
            self.trade_history.append({
                'time': self.market.get_time(),
                'signal': signal,
                'price': price,
                'position': self.position   
            })
    
    def get_equity(self, price):
        """
        Formalised function to calculate `equity`
        """
        return self.cash + self.position * price

    def update_position(self, signal : Move, price) -> None:
        """
        Changes portfolio position via `self.position` based on a generated signal.
        """
        equity = self.get_equity(price)

        # Check margin and equity to ensure we can afford the trades
        if signal == Move.BUY and self.cash < price + price * self.commission:
            return  # cannot afford to buy
        if signal == Move.SELL and equity < 0:
            self.close_position(price)
            return  # forced liquidation

        target_position = self.position

        if signal == Move.BUY:
            target_position = 1
        elif signal == Move.SELL:
            target_position = -1
        else:
            return

        if target_position == self.position:
            return

        self.close_position(price)

        if target_position == 1:
            if self.cash < price:
                return
            self.position = 1
            self.cash -= price
            self.cash -= price * self.commission
        elif target_position == -1:
            self.position = -1
            self.cash += price
            self.cash -= price * self.commission    
    
    def close_position(self, price) -> None:
        """
        Either offloads or buys up stock to make a position neutral.
        """
        if self.position > 0:
            self.cash += self.position * price
            self.cash -= price * self.commission
        elif self.position < 0:
            self.cash -= self.position * price
            self.cash -= price * self.commission
        self.position = 0
    
    def get_trade_history(self) -> list:
        """
        Simple retrieval function for `self.trade_history`
        """
        return self.trade_history
    
    def get_equity_history(self) -> list:
        """
        Simple retrieval function for `self.trade_history`
        """
        return self.equity_history

if __name__ == "__main__":
    market = GBMMarket(-0.07, 0.15, 100, dt=1/252)
    strategy = MomentumStrategy(lookback=20, threshold=2)
    portfolio = Portfolio(200, strategy, market, 0.01, 0.01)
    start_portfolio = f"Cash: ${portfolio.cash:.2f} | Position: {portfolio.position}"

    for _ in range(252):
        market.step()
        portfolio.update_portfolio()
    
    trade_history = pd.DataFrame(portfolio.get_trade_history())
    print(trade_history)
    print("\n---STARTING STATE---\n")
    print(start_portfolio)
    print("\n---FINAL STATE---\n")
    print(portfolio)
    print("\n---FINAL EQUITY---\n")
    print(f"Equity: ${portfolio.get_equity(market.get_price()):.2f}")
    
    

