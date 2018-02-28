from market_state import MarketState
from payoff_functions import VanillaOptionTerms, LookbackOptionTerms, AsianOptionTerms

# market states
mkt_state = MarketState(4, 1/4, 2, 1/2)

# vanilla option terms
vanilla_call_terms = VanillaOptionTerms(5, "c", 2)
vanilla_put_terms = VanillaOptionTerms(5, "p", 3)
intrinsic_call_terms = VanillaOptionTerms(5, "call", 0)
one_step_call_terms = VanillaOptionTerms(5, "call", 1)

# exotic option terms
lookback_terms = LookbackOptionTerms(3)
asian_call_terms = AsianOptionTerms(4, "c", 3)
asian_put_terms = AsianOptionTerms(5, "p", 4)
