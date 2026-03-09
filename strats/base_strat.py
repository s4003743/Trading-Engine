from enum import Enum
from market.gbm import GBMMarket

class Move(Enum):
    BUY = 1
    HOLD = 0
    SELL = -1

class Strategy():   
    def generate_signal(self, market):
        raise NotImplementedError