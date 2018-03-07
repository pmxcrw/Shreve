from unittest import TestCase
from markov_states import SimpleState, MaximumState, TotalState
from tests.test_fixtures import mkt_state


class TestSimpleState(TestCase):

    def test_state_tree(self):
        expected = [{4: (8, 2)},
                    {2: (4, 1), 8: (16, 4)},
                    {1: (2, 0.5), 4: (8, 2), 16: (32, 8)}]
        self.assertEqual(expected, SimpleState(mkt_state).state_tree(3).data)


class TestMaximumState(TestCase):

    def test_next_state(self):
        expected = [{(4, 4): ((8, 8), (2, 4))},
                    {(2, 4): ((4, 4), (1, 4)), (8, 8): ((16, 16), (4, 8))},
                    {(1, 4): ((2, 4), (0.5, 4)), (4, 4): ((8, 8), (2, 4)), (4, 8): ((8, 8), (2, 8)),
                     (16, 16): ((32, 32), (8, 16))}]
        self.assertEqual(expected, MaximumState(mkt_state).state_tree(3).data)


class TestTotalState(TestCase):

    def test_next_state(self):
        expected = [{(4, 4): ((8, 12), (2, 6))},
                    {(2, 6): ((4, 10), (1, 7)), (8, 12): ((16, 28), (4, 16))},
                    {(1, 7): ((2, 9), (0.5, 7.5)), (4, 10): ((8, 18), (2, 12)), (4, 16): ((8, 24), (2, 18)),
                     (16, 28): ((32, 60), (8, 36))}]
        self.assertEqual(expected, TotalState(mkt_state).state_tree(3).data)
