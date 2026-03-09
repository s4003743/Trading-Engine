import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class GBMMarket:
    def __init__(self, mu, sigma, S0, dt:float=1, seed_num=None):
        if seed_num is not None:
            np.random.seed(seed_num)

        self.mu = mu
        self.sigma = sigma
        self.price = S0
        self.dt = dt
        self.price_history = [S0]

    def step(self) -> float:
        """
        Iterates to a new price value which is dependant on the previous. 
        Returns new price value (float) and appends it to `self.history`. 
        Uses geometric brownian motion to model price changes. 
        """
        z = np.random.normal()
        self.price *= np.exp((self.mu - 0.5 * self.sigma**2) * self.dt + self.sigma * z * np.sqrt(self.dt))        
        self.price_history.append(self.price)
        return self.price
    
    def get_log_returns(self, n=None) -> list:
        """
        Using the formula `ret = log(P_t / P_t-1)` this function returns 
        the total log return for `self.price_history`. Please note that 
        since a return cannot be calculated for the first value, 
        `len(log_returns) = len(price_history) - 1` and starts at index 
        1 on `self.price_history`. 
        
        Also note that `n` represents the number of elements you want to 
        retrieve from the present (e.g. the last 5 log returns would be 
        n = 5). By default it will return the entire history.
        """
        log_history = []

        for i in range(1, len(self.price_history)):
            log_history.append(np.log(self.price_history[i] / self.price_history[i - 1]))
        
        if n is None:
            return log_history
        else:
            return log_history[-n:] 
    
    def get_price(self) -> float:
        """
        Formal retrieval of price. Simply returns `self.price`.
        """
        return self.price
    
    def get_time(self) -> int:
        """
        Returns the index of the current price.
        """
        return len(self.price_history) - 1
    
    def get_price_history(self, n=None) -> list:
        """
        Formal retrieval of price history. Simply returns `self.price_history`. 
        Can adjust how many prices to look back on using `n` parameter.
        """
        if n is None:
            return self.price_history
        else:
            return self.price_history[-n:]
        
if __name__ == "__main__":
    market = GBMMarket(0.07, 0.15, 100, 1/252)

    for _ in range(252):
        market.step()

    price_history = pd.DataFrame(market.get_price_history())
    price_history.plot(legend=False, figsize=(10, 5))
    plt.show()