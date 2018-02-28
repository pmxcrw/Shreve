# This is the version of the Markov States class that supports the recursion based valuation

from abc import ABC, abstractmethod
from market_state import MarketState


class BaseState(ABC):

    def __init__(self, initial_value, depth=0, up=None, down=None):
        if isinstance(initial_value, MarketState):
            msg = "if initialising with a MarketState all other values are derived from the MarketState"
            assert up is None and down is None and depth == 0, msg
            self.state_values = self._initial_state_values(initial_value.underlying_price)
            self.up = initial_value.up
            self.down = initial_value.down
            self.depth = 0
        else:
            self.state_values = initial_value
            self.up = up
            self.down = down
            self.depth = depth

    def __hash__(self):
        return hash((self.state_values, self.up, self.down, self.depth))

    def __eq__(self, other):
        return self.state_values == other.state_values and \
               self.up == other.up and \
               self.down == other.down and \
               self.depth == other.depth

    def __repr__(self):
        return "{}(({!r}, {!r}, {!r}, {!r})".format(self.__class__.__name__, self.state_values, self.depth,
                                                    self.up, self.down)

    @property
    @abstractmethod
    def next_state(self):
        pass

    @abstractmethod
    def _initial_state_values(self, initial_price):
        pass


class SimpleState(BaseState):

    @property
    def next_state(self):
        return SimpleState(self.state_values * self.up, self.depth + 1, self.up, self.down), \
               SimpleState(self.state_values * self.down, self.depth + 1, self.up, self.down)

    def _initial_state_values(self, initial_price):
        return initial_price


class MaximumState(BaseState):

    @property
    def next_state(self):
        state_up = self.state_values[0] * self.up, max(self.state_values[1], self.state_values[0] * self.up)
        state_down = self.state_values[0] * self.down, max(self.state_values[1], self.state_values[0] * self.down)
        return MaximumState(state_up, self.depth + 1, self.up, self.down), \
            MaximumState(state_down, self.depth + 1, self.up, self.down)

    def _initial_state_values(self, initial_price):
        return initial_price, initial_price


class TotalState(BaseState):

    @property
    def next_state(self):
        state_up = self.state_values[0] * self.up, self.state_values[1] + self.state_values[0] * self.up
        state_down = self.state_values[0] * self.down, self.state_values[1] + self.state_values[0] * self.down
        return TotalState(state_up, self.depth + 1, self.up, self.down), \
            TotalState(state_down, self.depth + 1, self.up, self.down)

    def _initial_state_values(self, initial_price):
        return initial_price, initial_price
