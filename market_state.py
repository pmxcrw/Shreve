import numpy as np


class MarketState(object):

    def __init__(self, underlying_price, interest_rate, up, down):
        self.underlying_price = underlying_price
        self.jumps = np.array([max(up, down), min(up, down)])
        self.rate = interest_rate
        assert 0 < down < 1 + self.rate < up, "the market is in arbitrage"
        p = (1 + self.rate - down) / (up - down)
        self.probabilities = np.array([p, 1-p])

    def __str__(self):
        return "Market state with underlying_price={}, interest_rate={}, " \
               "moves up={} and down={}".format(self.underlying_price, self.rate, self.jumps[0], self.jumps[1])

    def __repr__(self):
        return "{}(underlying={!r}, rate={!r}, jumps={!r})".format(self.__class__.__name__, self.underlying_price,
                                                   self.rate, self.jumps)
