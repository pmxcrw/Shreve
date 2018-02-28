# this is a nice way of coding the logic, using recursion, but hits a recursion depth limit quickly (960 steps)
# and is too slow


class EuropeanExerciseBinomial(object):

    def __init__(self, payoff_terms, market_state, step_size=1):
        self.payoff_terms = payoff_terms
        self.initial_state = payoff_terms.markov_state_class(market_state)
        self.df = 1 / (1 + market_state.rate)
        self.p = market_state.p
        self.q = market_state.q
        self.num_steps = payoff_terms.maturity * step_size
        self.node_cache = {}

    def __repr__(self):
        return "{}({!r}, initial_state={!r}, p={!r}, q={!r}, num_steps={!r})"\
            .format(self.__class__.__name__, self.payoff_terms, self.initial_state, self.p, self.q, self.num_steps)

    @property
    def price(self):
        return self._price(self.initial_state)

    def _price(self, state):
        if state in self.node_cache:
            return self.node_cache[state]
        else:
            if state.depth == self.num_steps:
                value = self.payoff_terms.payoff(state.state_values)
            else:
                next_state = state.next_state
                value = self.df * (self.p * self._price(next_state[0])
                                   + self.q * self._price(next_state[1]))
            self.node_cache[state] = value
            return value
