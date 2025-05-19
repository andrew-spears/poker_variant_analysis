Analysis of poker variants and simple hands, using analytical tools and numerical algorithms.

Analysis of a limit variant of von neumann poker:
https://github.com/tirantfox/poker_variant_analysis/blob/main/notebooks/limit_continuous_poker/solve_limit_continuous.ipynb

No-limit continuous poker desmos widget:
https://www.desmos.com/calculator/palhen19nj

Limit continuous poker desmos widget:
https://www.desmos.com/calculator/riicxq0xso

TODO:

- b0 is just x0 with some scaling factor!!!
- PROVE THEOREM: c(v_inv(x)) is increasing in U for all x> vth and forall U.

DONE:

- find the expected payoff of each x (specifically x2 and x3)
  - continuous and monotonic!
  - Easily integrable, gives a nicer derivation of the value function
  - solve for the x such that payoff(x, L, U) = value(L, U)
- Find a strategy profile which the bettor can deviate to without changing payoffs, which makes the value easier to solve
  - bluff size doesnt matter - always min bluff!
- For L=0, U variable, how does changing U affect the strategies and EV(x)?
  - x3 increasing in U, so the bettor value bets less with higher max
  - EV(x) for a fixed x increases until some point as U increases, then decreases... why?
    - Plausible explanation:
      - With a higher U, the bettor makes bigger bets.
      - bigger bets have worse pot odds, so they need more bluffs to balance to get called.
      - more bluffs means a wider bluffing range, so x2 increases (this does not mean that every bet size or every hand has to bluff more, only that there are more total bluffing hands).
      - as x2 increases, the caller has to call less often. Otherwise, the bettor could get away with bluffing less. Specifically, at x=x2, the bettor would rather check than bluff if the caller is calling too much.
      - If the caller calls less often, they must do this for all bet sizes s to avoid being exploited, so the entire c(s) curve shifts up.
      - c(s) is increasing in s, so shifting up means that sometimes even a smaller bet is less likely to be called.
      - because the caller calls less often, the bettor has a thinner value range (the entire v(s) curve shifts up).
      - this means the bettor bets less with the same hand strength.
      - for all value bets, it turns out that the bettor will still be called less often (that is, the decrease in bet size is not enough to offset the increase in c(s)).
      - Two factors combine: a smaller bet, called less often, means the bettor's EV(x) decreases.
      - So, in some cases, increasing U actually decreases the bettor's EV(x) for certain specific hand strengths. On average, however, it must increase EV(x) for a random hand strength because the value of the game is higher.
    - To test:
      - x for which this happens should be exactly the ones which bet smaller but get called less often.
    - results:
      - Every x has some U' such that EV(x) is decreasing in U for U > U'.
      - This U' is increasing in x (looks exponential).
      - For U > U' but fixed x, the bettor bets less, and the caller calls less.
      - For U < U', the bettor bets more, and the caller calls more.
        -THEOREM: c(s(x)) is increasing in U for all x> vth and forall U.
        - U' is just the U such that v_inv(x) = U'
