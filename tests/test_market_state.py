import numpy as np

from unittest import TestCase
from market_state import MarketState
from tests.test_fixtures import mkt_state


class TestInit(TestCase):
    def test_probabilities(self):
        np.allclose(mkt_state.probabilities, [0.5, 0.5])


class TestAssert(TestCase):
    def test_assert(self):
        self.assertRaises(AssertionError, MarketState, 2, 1, -1, 2)
        self.assertRaises(AssertionError, MarketState, 2, 0.25, 1.1, 0.5)
        self.assertRaises(AssertionError, MarketState, 2, 0.25, 2, 3)
