from unittest import TestCase
from binomial_valuations import EuropeanExerciseBinomialPriceable
from tests.test_fixtures import mkt_state, one_step_call_terms, vanilla_put_terms, lookback_terms, asian_call_terms


class TestOneStep(TestCase):

    def test_value(self):
        binomial_priceable = EuropeanExerciseBinomialPriceable(one_step_call_terms, mkt_state)
        self.assertAlmostEqual(1.2, binomial_priceable.price)


class TestMultiStep(TestCase):

    def test_value(self):
        binomial_priceable = EuropeanExerciseBinomialPriceable(vanilla_put_terms, mkt_state)
        self.assertAlmostEqual(0.864, binomial_priceable.price)


class TestLookback(TestCase):

    def test_value(self):
        binomial_priceable = EuropeanExerciseBinomialPriceable(lookback_terms, mkt_state)
        self.assertAlmostEqual(1.376, binomial_priceable.price)


class TestAsian(TestCase):

    def test_value(self):
        binomial_priceable = EuropeanExerciseBinomialPriceable(asian_call_terms, mkt_state)
        self.assertAlmostEqual(1.216, binomial_priceable.price)
