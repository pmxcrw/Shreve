from abc import ABC, abstractmethod


class BaseState(ABC):

    def __init__(self, mkt_state):
        self.initial_state = self._initial_state(mkt_state.underlying_price)
        self.up = mkt_state.up
        self.down = mkt_state.down

    def state_tree(self, depth):
        state_tree = [{self.initial_state: self.next_state(self.initial_state)}]
        for step in range(depth-1):
            current_states = set().union(*(set(states) for states in state_tree[step].values()))
            state_transitions = {state: self.next_state(state) for state in current_states}
            state_tree.append(state_transitions)
        return state_tree

    def __repr__(self):
        return "{}(({!r}, {!r}, {!r})".format(self.__class__.__name__, self.initial_state, self.up, self.down)

    @abstractmethod
    def next_state(self, current_state):
        pass

    @abstractmethod
    def _initial_state(self, initial_price):
        pass


class SimpleState(BaseState):

    def next_state(self, current_state):
        return current_state * self.up, current_state * self.down

    def _initial_state(self, initial_price):
        return initial_price


class MaximumState(BaseState):

    def next_state(self, current_state):
        asset_up = current_state[0] * self.up
        asset_down = current_state[0] * self.down
        state_up = asset_up, max(current_state[1], asset_up)
        state_down = asset_down, max(current_state[1], asset_down)
        return state_up, state_down

    def _initial_state(self, initial_price):
        return initial_price, initial_price


class TotalState(BaseState):

    def next_state(self, current_state):
        asset_up = current_state[0] * self.up
        asset_down = current_state[0] * self.down
        state_up = asset_up, current_state[1] + asset_up
        state_down = asset_down, current_state[1] + asset_down
        return state_up, state_down

    def _initial_state(self, initial_price):
        return initial_price, initial_price


class CompoundState(BaseState):

    def next_state(self, current_state):
        pass

    def _initial_state(self, initial_price):
        pass
