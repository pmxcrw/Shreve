from unittest import TestCase
from market_state import MarketState
from tests.test_fixtures import mkt_state


class TestInit(TestCase):
    def test_p(self):
        self.assertEqual(mkt_state.p, 1 / 2)

    def test_q(self):
        self.assertEqual(mkt_state.q, 1 / 2)


class TestAssert(TestCase):
    def test_assert(self):
        self.assertRaises(AssertionError, MarketState, 2, 1, -1, 2)
        self.assertRaises(AssertionError, MarketState, 2, 0.25, 1.1, 0.5)
        self.assertRaises(AssertionError, MarketState, 2, 0.25, 2, 3)
