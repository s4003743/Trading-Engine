import numpy as np

class GBMMarket:
    def __init__(self, mu, sigma, S0):
        self.mu = mu
        self.sigma = sigma
        self.price = S0

    def step(self):
        z = np.random.normal()
        self.price *= np.exp((self.mu - 0.5*self.sigma**2) + self.sigma*z)
        return self.price