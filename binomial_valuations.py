

class EuropeanExerciseBinomialPriceable(object):

    def __init__(self, payoff_terms, market_state, step_size=1):
        self.payoff_terms = payoff_terms
        self.num_steps = payoff_terms.maturity * step_size
        self.state_tree = payoff_terms.markov_state_class(market_state).state_tree(self.num_steps)
        self.df = 1 / (1 + market_state.rate)
        self.p = market_state.p
        self.q = market_state.q

    def __repr__(self):
        return "{}({!r}, num_steps={!r})"\
            .format(self.__class__.__name__, self.payoff_terms, self.num_steps)

    @property
    def price(self):
        # get the final states from the end of the state_tree, as a set to avoid duplicate payoff calculations and
        # shorten the next loop.
        final_states = set().union(*(set(states) for states in self.state_tree[-1].values()))
        # map between final states and their payoff
        value_dict = {state: self.payoff_terms.payoff(state) for state in final_states}
        # backward induction, calculating the discounted expected future payoff.
        discounted_p = self.df * self.p
        discounted_q = self.df * self.q
        for step in range(1, self.num_steps+1):
            value_dict = {state: discounted_p * value_dict[next_state[0]] + discounted_q * value_dict[next_state[1]]
                          for (state, next_state) in self.state_tree[-step].items()}
        return list(value_dict.values())[0]
