# Poker Variant Analysis

Analysis of poker variants and simple hands, using analytical tools and numerical algorithms.

## Limit Continuous Poker: Key Results

This repository contains research on **Limit Continuous Poker (LCP)**, a game-theoretic model that bridges two classical poker variants by imposing lower and upper bounds (L and U) on bet sizes. Our analysis reveals surprising mathematical structure and strategic insights about optimal betting and bluffing.

### Main Contributions

**1. Nash Equilibrium Strategy Profile**

We derive the unique admissible Nash equilibrium where:

- The **bettor** partitions hands into three regions: bluffing with weak hands [0, x₂], checking with medium hands [x₂, x₃], and value betting with strong hands [x₃, 1]
- Bet sizes vary continuously within bluffing and value ranges (weaker bluffs use larger bets!)
- The **caller** responds with a bet-size-dependent calling threshold that perfectly balances pot odds

![LCP Strategy Profile](latex/limit_continuous_poker/sections/nash_equilibrium/images/LCP_profile_0.3_1.5.png)

**2. Closed-Form Game Value with Remarkable Symmetry**

The expected payoff for the bettor has a surprisingly elegant formula:

```
V(r,t) = (1 - r³ - t³) / (14 - 2r³ - 2t³)
```

where r = L/(1+L) (minimum pot odds) and t = 1/(1+U) (pot fraction at max bet).

**Key discovery:** The value function exhibits perfect symmetry V(r,t) = V(t,r), meaning that swapping minimum and maximum bet constraints in a specific reciprocal way (V(L,U) = V(1/U, 1/L)) yields identical game values. This reveals a deep duality between the caller's incentive to call and the bettor's betting freedom.

![Game Value Heatmaps](latex/limit_continuous_poker/sections/game_value/images/game_value_plots.png)

**3. Counterintuitive Strategic Effects**

Increasing the maximum bet size U doesn't uniformly benefit all hands:

- **Strong hands** gain from making larger value bets
- **Intermediate hands** can actually _lose_ value because the caller becomes more conservative across all bet sizes
- Each hand strength x has a critical threshold U' above which EV(x) decreases

This illustrates the complex strategic interdependencies in equilibrium play—more options can sometimes hurt!

![Expected Payoffs by Hand Strength](latex/limit_continuous_poker/sections/payoff_analysis/images/ExpectedPayoffs.png)

**4. Convergence to Classical Variants**

LCP smoothly interpolates between:

- **Fixed-Bet Continuous Poker (FBCP):** As L → B and U → B, strategies converge to von Neumann's solution
- **No-Limit Continuous Poker (NLCP):** As L → 0 and U → ∞, strategies converge to the solution by Chen & Ankenman

This validates LCP as a genuine unified framework encompassing both classical models.

### Resources

- **Paper (PDF):** [latex/limit_continuous_poker/main/main.pdf](latex/limit_continuous_poker/main/main.pdf)
- **Numerical Analysis:** [notebooks/limit_continuous_poker/solve_limit_continuous.ipynb](notebooks/limit_continuous_poker/solve_limit_continuous.ipynb)
- **Interactive Widgets:**
  - [No-limit continuous poker (Desmos)](https://www.desmos.com/calculator/palhen19nj)
  - [Limit continuous poker (Desmos)](https://www.desmos.com/calculator/riicxq0xso)

---

### Von Neumann Poker

Von Neumann poker (also called Continous poker) is a simplified model of poker. It is a two-player zero-sum game designed to study strategic decision-making in competitive environments. The game abstracts away many complexities of real poker, focusing instead on the mathematical and strategic aspects of bluffing, betting, and optimal play.

The original game works as follows:

- The game involves only two players, often referred to as the bettor and the caller.
- Players are each dealt a real number uniformly and independently from the interval [0, 1]
- The game consists of a single 'half-street' of betting, where the bettor chooses between checking and betting a fixed amount $s$, but the caller can only call or fold (no raising, and a check by the bettor goes straight to showdown).
- In showdown, the higher hand strength wins.

Von Neumann poker has a solved Nash equilibrium strategy profile discussed here: http://datagenetics.com/blog/december32018/index.html

What if we allow the bettor to choose a bet size $s$?

A variant where $s$ can be any nonnegative real number is called No-limit Continuous Poker, discussed and solved here (page 154 of "The Mathematics of Poker" by Bill Chen and Jerrod Ankenman): https://www.pokerbooks.lt/books/en/The_Mathematics_of_Poker.pdf

### Limit Continuous Poker

We now consider the variant where $s$ is bounded by an upper limit $U$ and lower limit $L$, referred to as the max and min bets. We will call this variant Limit Continuous Poker.

To fully describe the rules:

- Two players: bettor and caller (or I and II).
- Players are each dealt a real number uniformly and independently from the interval [0, 1]
- A single 'half-street' of betting: the bettor chooses between checking and betting a fixed amount $s \in [L, U]$; if a bet is made, the caller either calls or folds.
- In showdown, the higher hand strength wins.

We attempt to answer the following questions:

- What is the Nash equilibrium strategy profile for Limit Continuous Poker?
- What is the value of the game, and does the bettor have the upper hand still (as in No-limit Continuous Poker)? If so, is there a simple strategic argument for why the bettor must win in expectation?
- As the bounds $L$ and $U$ change, how does the strategy profile change? Does this reflect observed behavior in real poker games with minimum and maximum bet sizes?
- As the bounds $L$ and $U$ approach 0 and $\infty$, respectively, does the strategy profile approach the Nash equilibrium of No-limit Continuous Poker?
- As the bounds $L$ and $U$ approach some fixed value $s$ from either side, does the strategy profile approach the Nash equilibrium of Continuous Poker with fixed bet size $s$?

TODO:

- Introduction:
- ## Game value:
- b0 is just x0 with some scaling factor!!!
- PROVE THEOREM: c(v_inv(x)) is increasing in U for all x> vth and forall U

DONE:

- find the expected payoff of each x (specifically x2 and x3)
  - continuous and monotonic in x
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
