from unittest import TestCase
from payoff_functions import VanillaOptionTerms
from tests.test_fixtures import vanilla_call_terms, vanilla_put_terms, lookback_terms, asian_put_terms


class TestVanillaOption(TestCase):

    def test_put(self):
        self.assertEqual(vanilla_put_terms.payoff(8), 0)
        self.assertEqual(vanilla_put_terms.payoff(3), 2)

    def test_call(self):
        self.assertEqual(vanilla_call_terms.payoff(8), 3)
        self.assertEqual(vanilla_call_terms.payoff(5), 0)

    def test_error(self):
        self.assertRaises(ValueError, VanillaOptionTerms, 5, "x", 2)
        self.assertRaises(AssertionError, VanillaOptionTerms, 5, 3, 2)


class TestLookbackOption(TestCase):

    def test_payoff(self):
        self.assertEqual(lookback_terms.payoff((2, 8)), 6)


class TestAsianOption(TestCase):

    def test_put(self):
        self.assertEqual(asian_put_terms.payoff((8, 20)), 1)
        self.assertEqual(asian_put_terms.payoff((32, 60)), 0)
