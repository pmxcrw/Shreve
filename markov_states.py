from abc import ABC, abstractmethod
from tree import Tree


class BaseState(ABC):

    def __init__(self, mkt_state):
        self.initial_state = self._initial_state(mkt_state.underlying_price)
        self.jumps = mkt_state.jumps

    def state_tree(self, depth):
        state_tree = Tree(self.initial_state, self.next_state)
        state_tree.extend(depth)
        return state_tree

    def next_prices(self, current_price):
        return current_price * self.jumps

    def __repr__(self):
        return "{}((initial_state={!r}, jumps={!r})".format(self.__class__.__name__, self.initial_state, self.jumps)

    @abstractmethod
    def next_state(self, current_state, depth=0):
        pass

    @abstractmethod
    def _initial_state(self, initial_price):
        pass


class SimpleState(BaseState):

    def next_state(self, current_state, depth=0):
        return tuple(self.next_prices(current_state))

    def _initial_state(self, initial_price):
        return initial_price


class MaximumState(BaseState):

    def __init__(self, mkt_state, start=0):
        self.start = start
        super().__init__(mkt_state)

    def next_state(self, current_state, depth=0):
        next_prices = self.next_prices(current_state[0])
        state_up = next_prices[0], max(current_state[1], next_prices[0])
        state_down = next_prices[1], max(current_state[1], next_prices[1])
        return state_up, state_down

    def _initial_state(self, initial_price):
        return initial_price, initial_price


class TotalState(BaseState):

    def next_state(self, current_state, depth=0):
        next_prices = self.next_prices(current_state[0])
        state_up = next_prices[0], current_state[1] + next_prices[0]
        state_down = next_prices[1], current_state[1] + next_prices[1]
        return state_up, state_down

    def _initial_state(self, initial_price):
        return initial_price, initial_price
