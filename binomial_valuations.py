

class EuropeanExerciseBinomialPriceable(object):

    def __init__(self, payoff_terms, market_state, step_size=1):
        self.payoff_terms = payoff_terms
        self.num_steps = payoff_terms.maturity * step_size
        self.state_tree = payoff_terms.markov_state_class(market_state).state_tree(self.num_steps)
        self.discounted_probabilities = 1 / (1 + market_state.rate) * market_state.probabilities
        self.initial_transition = list(self.state_tree[0].values())[0] # the possible outcomes of the first branch
        self.delta_cache = None

    def __repr__(self):
        return "{}({!r}, num_steps={!r})"\
            .format(self.__class__.__name__, self.payoff_terms, self.num_steps)

    @property
    def price(self):
        final_states = self.state_tree.terminal_states
        # map between final states and their payoff
        value_dict = {state: self.payoff_terms.payoff(state) for state in final_states}
        # backward induction, calculating the discounted expected future payoff.
        for step in range(1, self.num_steps):
            value_dict = {state: self._induction_calculation(value_dict, next_state)
                          for (state, next_state) in self.state_tree[-step].items()}
        self.delta_cache = value_dict
        final_price = self._induction_calculation(value_dict, self.initial_transition)
        return final_price

    def _induction_calculation(self, value_dict, next_state):
        return self.discounted_probabilities[0] * value_dict[next_state[0]] + \
               self.discounted_probabilities[1] * value_dict[next_state[1]]

    @property
    def delta(self):
        if self.delta_cache is None:
           _ = self.price
        initial_prices = self._get_prices(self.initial_transition)
        value_dict = self.delta_cache
        delta = (value_dict[self.initial_transition[0]] - value_dict[self.initial_transition[1]]) / \
                (initial_prices[0] - initial_prices[1])
        return delta

    def _get_prices(self, state):
        if type(state[0]) is tuple:
            return state[0][0], state[1][0]
        return state
