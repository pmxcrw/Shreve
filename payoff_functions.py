import numpy as np

from abc import ABC, abstractmethod
from markov_states import SimpleState, MaximumState, TotalState


class BaseOptionTerms(ABC):

    def __init__(self, maturity):
        self.maturity = maturity
        self.markov_state_class = self._set_markov_state_class

    @abstractmethod
    def payoff(self, state):
        pass

    @property
    @abstractmethod
    def _set_markov_state_class(self):
        pass

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.maturity)


class VanillaOptionTerms(BaseOptionTerms):

    def __init__(self, strike, put_call, maturity):
        super().__init__(maturity)
        self.strike = strike
        put_aliases = {"PUT", "P"}
        call_aliases = {"CALL", "C"}
        assert type(put_call) == str
        self.put_call = put_call.upper()
        if self.put_call in put_aliases:
            self._payoff = lambda state: np.maximum(self.strike - state, 0)
        elif self.put_call in call_aliases:
            self._payoff = lambda state: np.maximum(state - self.strike, 0)
        else:
            raise ValueError("put_call type not recognised")

    def payoff(self, state):
        return self._payoff(state)

    @property
    def _set_markov_state_class(self):
        return SimpleState

    def __repr__(self):
        return "{}({!r}, {!r}, {!r})".format(self.__class__.__name__, self.strike, self.put_call, self.maturity)


class LookbackOptionTerms(BaseOptionTerms):

    def payoff(self, state):
        return state[1] - state[0]

    @property
    def _set_markov_state_class(self):
        return MaximumState


class AsianOptionTerms(VanillaOptionTerms):

    def payoff(self, state):
        average = state[1] / (1 + self.maturity)
        return super().payoff(average)

    @property
    def _set_markov_state_class(self):
        return TotalState
