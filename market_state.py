class MarketState(object):

    def __init__(self, underlying_price, interest_rate, up, down):
        self.underlying_price = underlying_price
        self.up = max(up, down)
        self.down = min(up, down)
        self.rate = interest_rate
        assert 0 < self.down < 1 + self.rate < self.up, "the market is in arbitrage"
        self.p = (1 + self.rate - self.down) / (self.up - self.down)
        self.q = 1 - self.p

    def __str__(self):
        return "Market state with underlying_price={}, interest_rate={}, " \
               "moves up={} and down={}".format(self.underlying_price, self.rate, self.up, self.down)

    def __repr__(self):
        return "{}({!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__, self.underlying_price,
                                                   self.rate, self.up, self.down)
