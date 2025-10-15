# %%
from game_utils.ContinuousPokerVariants.LCP import LCP

# %% 
import sympy as sp
from game_utils.ContinuousPokerVariants.LCP_symbolic import LCP_symbolic
cls = LCP_symbolic
LCP_symbolic.solve_neq()
LCP_symbolic.generate_strategy_plot(L=0.5, U=1.5)
# %% 
LCP_symbolic.call_threshold(s=1, L=0.5, U=1.5)

# %%
LCP_symbolic.bluff_threshold(L=0.5, U=1.5)

# %%
LCP_symbolic.value_threshold(L=0.5, U=1.5)

# %%
